const links = {
  live: "https://api-auctora.vercel.app/api/",
  local: 'http://localhost:8000/api/',
}

const current = links.live;

const capitalize = (s) => {
  if (typeof s !== 'string') return ''
  let newString = s.charAt(0).toUpperCase() + s.slice(1)
  return newString
};

const charLimit = (s, limit) => {
  if (typeof s !== 'string') return ''
  if (s.length > limit) {
    return s.slice(0, limit) + '...'
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
  charLimit,
  links,
  current
}