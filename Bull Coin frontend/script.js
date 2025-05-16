const backend = 'https://bull-coin-backend.subhanimranlong4566.repl.co'; // Replace this with your Replit backend

const walletTextarea = document.getElementById('wallet');

fetch(`${backend}/`)
  .then(() => {
    fetch(`${backend}/get_chain`)
      .then(res => res.json())
      .then(() => {
        fetch(`${backend}/`)
          .then(() => walletTextarea.value = "Wallet initialized on backend.");
      });
  });

function sendTransaction() {
  const receiver = document.getElementById('receiver').value;
  const amount = document.getElementById('amount').value;

  fetch(`${backend}/get_chain`)
    .then(res => res.json())
    .then(chain => {
      fetch(`${backend}/add_transaction`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sender: chain[0].transactions?.[0]?.receiver || 'unknown',
          receiver: receiver,
          amount: parseInt(amount),
          signature: ''
        })
      })
      .then(res => res.text())
      .then(data => document.getElementById('sendResponse').innerText = data);
    });
}

function mine() {
  fetch(`${backend}/mine_block`)
    .then(res => res.json())
    .then(data => {
      document.getElementById('mineResult').innerText = JSON.stringify(data, null, 2);
    });
}

function getChain() {
  fetch(`${backend}/get_chain`)
    .then(res => res.json())
    .then(data => {
      document.getElementById('chainData').innerText = JSON.stringify(data, null, 2);
    });
}
