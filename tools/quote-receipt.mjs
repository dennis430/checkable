#!/usr/bin/env node
// Build a genesis.receipt.v1 quotation for one exact occurrence of a string.
// Does not verify. Does not decide what the sentence means.
import { createHash } from 'node:crypto'
import { readFileSync } from 'node:fs'
import { pathToFileURL } from 'node:url'
import { parseArgs } from 'node:util'

export function quotationReceipt(bytes, needle, nth) {
  if (nth !== undefined && (!Number.isSafeInteger(nth) || nth < 1)) {
    return { ok: false, code: 64, error: 'nth must be a positive safe integer' }
  }
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
  if (nth === undefined && indexes.length !== 1) {
    return { ok: false, code: 2, error: `text occurs ${indexes.length} times; receipt not written` }
  }
  if (nth !== undefined && nth > indexes.length) {
    return { ok: false, code: 2, error: `occurrence ${nth} requested, but text occurs ${indexes.length} times; receipt not written` }
  }
  const start = indexes[nth === undefined ? 0 : nth - 1]
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
  let args
  try {
    args = parseArgs({ options: { nth: { type: 'string' } }, allowPositionals: true })
  } catch (error) {
    console.error(error.message)
    process.exit(64)
  }
  const [file, needle] = args.positionals
  if (!file || needle === undefined || args.positionals.length !== 2) {
    console.error('usage: quote-receipt [--nth <positive integer>] <file> <exact text>')
    process.exit(64)
  }
  if (args.values.nth !== undefined && !/^[1-9]\d*$/.test(args.values.nth)) {
    console.error('nth must be a positive safe integer')
    process.exit(64)
  }
  const result = quotationReceipt(readFileSync(file), needle, args.values.nth === undefined ? undefined : Number(args.values.nth))
  if (!result.ok) {
    console.error(result.error)
    process.exit(result.code)
  }
  process.stdout.write(`${JSON.stringify(result.receipt, null, 2)}\n`)
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) main()
