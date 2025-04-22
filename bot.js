const mineflayer = require('mineflayer');
const fs = require('fs');

const [,, host, port, version] = process.argv;

const bot = mineflayer.createBot({
  host,
  port: parseInt(port),
  version,
  username: "PozBot Original"
});

let currentPlayers = [];

bot.once('spawn', () => {
  bot.chat('/effect give @s minecraft:invisibility 999999 1 true');
  bot.chat('/list');

  setInterval(() => {
    bot.look(Math.random() * 2 * Math.PI, 0);
    bot.setControlState('jump', true);
    setTimeout(() => bot.setControlState('jump', false), 500);
    bot.setControlState('sneak', true);
    setTimeout(() => bot.setControlState('sneak', false), 1000);
  }, 10000);
});

bot.on('message', (msg) => {
  const text = msg.toString();
  if (text.includes('Çevrimiçi oyuncular')) {
    const match = text.match(/: (.*)/);
    if (match && match[1]) {
      currentPlayers = match[1].split(', ');
      fs.writeFileSync("players.json", JSON.stringify(currentPlayers));
    }
  }
});
