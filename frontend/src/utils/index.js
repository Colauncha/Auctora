const links = {
  live: "https://api-auctora.vercel.app/api/",
  local: 'http://localhost:8000/api/'
}

const capitalize = (s) => {
  if (typeof s !== 'string') return ''
  let newString = s.charAt(0).toUpperCase() + s.slice(1)
  return newString
};

const char20 = (s) => {
  console.log(s)
  if (typeof s !== 'string') return ''
  if (s.length > 20) {
    return s.slice(0, 20) + '...'
  } return s
};

const currencyFormat = (num) => {
  const kobo = (num % 1).toFixed(2).substring(2);
  const naira = Math.floor(num).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
  return `₦${naira}.${kobo}`;
}


export {
  capitalize,
  currencyFormat,
  char20,
  links
}