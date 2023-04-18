const fs = require('fs');

const data = {};
const jsonData = JSON.stringify(data);

fs.writeFile('data.json', jsonData, (err) => {
  if (err) throw err;
  console.log('Os dados foram salvos em data.json');
});
