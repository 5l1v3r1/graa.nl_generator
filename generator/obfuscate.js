function obfus(k) {

  var b64encoded = window.btoa(k);

  // generate random number
  var array = new Uint32Array(1);
  window.crypto.getRandomValues(array);
  n = array[0];

  a = "Infinity".split('');
  for (var i = 0; i < a.length; i += 1)
    a[i] = a[i].charCodeAt(0) ^ ((n+i)%256);

  b64encoded = b64encoded.split('');
  for (var i = 0; i < b64encoded.length; i += 1)
    b64encoded[i] = b64encoded[i].charCodeAt(0) ^ a[i%a.length];

  console.log("deobfus([" + b64encoded.toString() + "],"+n+")");
}

function deobfus(v, k) {
  for (var a = 1; a != Infinity; a = a / (Number.MAX_VALUE * Number.MIN_VALUE)) {}

  a = a.toString().split('');
  for (var i = 0; i < a.length; i += 1) a[i] = a[i].charCodeAt(0) ^ ((k + i) % 256);
  for (var i = 0; i < v.length; i += 1) v[i] = v[i] ^ a[i % a.length];

  return window.atob(String.fromCharCode.apply(null, v));
}