import assert from 'node:assert/strict'
import { test } from 'node:test'
import { quotationReceipt } from './quote-receipt.mjs'
import { mkdtempSync, writeFileSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { spawnSync } from 'node:child_process'

test('one exact occurrence becomes a quotation receipt', () => {
  const text = 'alpha\nbeta phrase\nalpha\n'
  const result = quotationReceipt(Buffer.from(text, 'utf8'), 'beta phrase')
  assert.equal(result.ok, true)
  assert.equal(result.receipt.derivation.span.start, Buffer.from('alpha\n', 'utf8').length)
  assert.equal(result.receipt.claim.text, 'beta phrase')
  assert.equal(result.receipt.derivation.expectedText, 'beta phrase')
  assert.equal(result.receipt.rule.id, 'quotation.exact')
})

test('missing text is not a receipt', () => {
  const result = quotationReceipt(Buffer.from('alpha', 'utf8'), 'nope')
  assert.equal(result.ok, false)
  assert.equal(result.code, 2)
})

test('two occurrences are not guessed', () => {
  const result = quotationReceipt(Buffer.from('same same', 'utf8'), 'same')
  assert.equal(result.ok, false)
  assert.match(result.error, /2 times/)
})

test('three copies require an explicit selector and nth 2 selects the second byte span', () => {
  const needle = 'The lantern is lit.'
  const bytes = Buffer.from(`é\n${needle}\ncontext\n${needle}\n${needle}\n`, 'utf8')
  assert.equal(quotationReceipt(bytes, needle).ok, false)
  const result = quotationReceipt(bytes, needle, 2)
  assert.equal(result.ok, true)
  const start = bytes.indexOf(needle, bytes.indexOf(needle) + 1)
  assert.deepEqual(result.receipt.derivation.span, { start, end: start + Buffer.byteLength(needle) })
  assert.equal(bytes.subarray(start, result.receipt.derivation.span.end).toString('utf8'), needle)
  assert.equal(quotationReceipt(bytes, needle, 4).ok, false)
  for (const nth of [0, -1, 1.5, NaN, Infinity, Number.MAX_SAFE_INTEGER + 1, '2']) {
    assert.equal(quotationReceipt(bytes, needle, nth).code, 64)
  }
})

test('CLI nth 2 passes genesis; ambiguous, invalid and out-of-range requests write no receipt', () => {
  const dir = mkdtempSync(join(tmpdir(), 'checkable-quote-'))
  try {
    const file = join(dir, 'three.txt'), receipt = join(dir, 'receipt.json')
    const needle = 'The lantern is lit.'
    writeFileSync(file, `${needle}\n${needle}\n${needle}\n`)
    const quote = (...args) => spawnSync(process.execPath, ['tools/quote-receipt.mjs', file, needle, ...args], { encoding: 'utf8' })
    const selected = quote('--nth', '2')
    assert.equal(selected.status, 0, selected.stderr)
    assert.equal(JSON.parse(selected.stdout).derivation.span.start, Buffer.byteLength(`${needle}\n`))
    writeFileSync(receipt, selected.stdout)
    const verified = spawnSync(process.execPath, ['packages/genesis-verifier/src/cli.mjs', file, receipt], { encoding: 'utf8' })
    assert.equal(verified.status, 0, verified.stderr)
    for (const args of [[], ['--nth', '4'], ['--nth', '0'], ['--nth', '-1'], ['--nth', '1.5'], ['--nth', '2oops'], ['--nth'], ['--nth', '9007199254740992']]) {
      const refused = quote(...args)
      assert.notEqual(refused.status, 0)
      assert.equal(refused.stdout, '')
    }
  } finally {
    rmSync(dir, { recursive: true, force: true })
  }
})
