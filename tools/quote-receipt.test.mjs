import assert from 'node:assert/strict'
import { test } from 'node:test'
import { quotationReceipt } from './quote-receipt.mjs'

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
