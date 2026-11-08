#!/usr/bin/env node
// Build a genesis.receipt.v1 quotation for one exact occurrence of a string.
// Does not verify. Does not decide what the sentence means.
import { createHash } from 'node:crypto'
import { readFileSync } from 'node:fs'
import { pathToFileURL } from 'node:url'

export function quotationReceipt(bytes, needle) {
  const needleBytes = Buffer.from(needle, 'utf8')
  if (needleBytes.length === 0) {
    return { ok: false, code: 64, error: 'text is empty' }
  }
  const indexes = []
  let from = 0
  while (from < bytes.length) {
    const at = bytes.indexOf(needleBytes, from)
    if (at === -1) break
    indexes.push(at)
    from = at + 1
  }
  if (indexes.length === 0) return { ok: false, code: 2, error: 'text not found' }
  if (indexes.length !== 1) {
    return { ok: false, code: 2, error: `text occurs ${indexes.length} times; receipt not written` }
  }
  const start = indexes[0]
  const end = start + needleBytes.length
  return {
    ok: true,
    code: 0,
    receipt: {
      receiptVersion: 'genesis.receipt.v1',
      rule: { id: 'quotation.exact', version: '1' },
      evidence: { sha256: createHash('sha256').update(bytes).digest('hex') },
      source: { kind: 'counterparty_supplied' },
      claimStanding: 'observed',
      claim: { text: needle },
      derivation: {
        type: 'quotation',
        span: { start, end },
        expectedText: needle,
      },
      limitations: [
        'GENUINENESS_NOT_ESTABLISHED',
        'SOURCE_KIND_IS_DECLARED_NOT_PROVEN',
        'SUBJECT_CONTROL_NOT_ESTABLISHED',
        'CLAIM_TEXT_IS_NOT_INTERPRETED_BEYOND_EXACT_MATCH',
      ],
    },
  }
}

function main() {
  const [file, needle] = process.argv.slice(2)
  if (!file || needle === undefined) {
    console.error('usage: quote-receipt <file> <exact text>')
    process.exit(64)
  }
  const result = quotationReceipt(readFileSync(file), needle)
  if (!result.ok) {
    console.error(result.error)
    process.exit(result.code)
  }
  process.stdout.write(`${JSON.stringify(result.receipt, null, 2)}\n`)
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) main()
