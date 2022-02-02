import { ethers } from 'ethers';
import { SignatureType, SiweMessage } from 'siwe';

// current page url
const domain = window.location.host;
// protocol, hostname and port number of the URL
const origin = window.location.origin;
// connect to ethereum network and sign transactions with Metamask
const provider = new ethers.providers.Web3Provider(window.ethereum);
const signer = provider.getSigner();

const BACKEND_ADDR = "http://localhost:5000";

// connect to Metamask
function connectWallet() {
    provider.send('eth_requestAccounts', [])
        .catch(() => console.log('user rejected request'));
}

async function signInWithEthereum() {
    // create siwe message and call backend to get a nonce
    const res1 = await fetch(`${BACKEND_ADDR}/nonce`, {
        credentials: 'include',
    });
    const message = new SiweMessage({
        domain: domain,
        address: await signer.getAddress(),
        statement: 'Sign in with Ethereum to the app.',
        uri: origin,
        version: '1',
        chainId: '1',
        nonce: await res1.text()
    });

    const signature = await signer.signMessage(message.signMessage());
    message.signature = signature;

    // post message and signature to backend where it will be verified
    const res2 = await fetch(`${BACKEND_ADDR}/verify`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message, signature }),
        credentials: 'include'
    });
    console.log(await res2.text());
}

// once authenticated we can pull some user data using the siwe package
async function getInformation() {
    const res = await fetch(`${BACKEND_ADDR}/personal_information`, {
        credentials: 'include',
    });
    console.log(await res.text());
}

const connectWalletBtn = document.getElementById('connectWalletBtn');
const siweBtn = document.getElementById('siweBtn');
const infoBtn = document.getElementById('infoBtn');
connectWalletBtn.onclick = connectWallet;
siweBtn.onclick = signInWithEthereum;
infoBtn.onclick = getInformation;
