import moment from 'moment'

export function parseTime (time, format) {
  return moment(time).format(format)
}

export function fileSizeToString (size) {
  const b = /^(b|B)$/
  const symbol = {
    iec: {
      bits: ['b', 'Kib', 'Mib', 'Gib', 'Tib', 'Pib', 'Eib', 'Zib', 'Yib'],
      bytes: ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
    },
    jedec: {
      bits: ['b', 'Kb', 'Mb', 'Gb', 'Tb', 'Pb', 'Eb', 'Zb', 'Yb'],
      bytes: ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    }
  }

  var descriptor = arguments.length <= 1 || arguments[1] === undefined ? {} : arguments[1]

  var result = []
  var val = 0
  var e = void 0
  var base = void 0
  var bits = void 0
  var ceil = void 0
  var neg = void 0
  var num = void 0
  var output = void 0
  var round = void 0
  var unix = void 0
  var spacer = void 0
  var standard = void 0
  var symbols = void 0

  if (isNaN(size)) {
    return ''
  }

  bits = descriptor.bits === true
  unix = descriptor.unix === true
  base = descriptor.base || 2
  round = descriptor.round !== undefined ? descriptor.round : unix ? 1 : 2
  spacer = descriptor.spacer !== undefined ? descriptor.spacer : unix ? '' : ' '
  symbols = descriptor.symbols || descriptor.suffixes || {}
  standard = base === 2 ? descriptor.standard || 'jedec' : 'jedec'
  output = descriptor.output || 'string'
  e = descriptor.exponent !== undefined ? descriptor.exponent : -1
  num = Number(size)
  neg = num < 0
  ceil = base > 2 ? 1000 : 1024

  // Flipping a negative number to determine the size
  if (neg) {
    num = -num
  }

  // Zero is now a special case because bytes divide by 1
  if (num === 0) {
    result[0] = 0
    result[1] = unix ? '' : !bits ? 'B' : 'b'
  } else {
    // Determining the exponent
    if (e === -1 || isNaN(e)) {
      e = Math.floor(Math.log(num) / Math.log(ceil))

      if (e < 0) {
        e = 0
      }
    }

    // Exceeding supported length, time to reduce & multiply
    if (e > 8) {
      e = 8
    }

    val = base === 2 ? num / Math.pow(2, e * 10) : num / Math.pow(1000, e)

    if (bits) {
      val *= 8

      if (val > ceil && e < 8) {
        val /= ceil
        e++
      }
    }

    result[0] = Number(val.toFixed(e > 0 ? round : 0))
    result[1] = base === 10 && e === 1 ? bits ? 'kb' : 'kB' : symbol[standard][bits ? 'bits' : 'bytes'][e]

    if (unix) {
      result[1] = standard === 'jedec' ? result[1].charAt(0) : e > 0 ? result[1].replace(/B$/, '') : result[1]

      if (b.test(result[1])) {
        result[0] = Math.floor(result[0])
        result[1] = ''
      }
    }
  }

  // Decorating a 'diff'
  if (neg) {
    result[0] = -result[0]
  }

  // Applying custom symbol
  result[1] = symbols[result[1]] || result[1]

  // Returning Array, Object, or String (default)
  if (output === 'array') {
    return result
  }

  if (output === 'exponent') {
    return e
  }

  if (output === 'object') {
    return {value: result[0], suffix: result[1], symbol: result[1]}
  }

  return result.join(spacer)
}
