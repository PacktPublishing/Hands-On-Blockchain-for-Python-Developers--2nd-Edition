import { useAccount, useConnect, useDisconnect, useSignMessage } from 'wagmi'
import { useState, useEffect } from 'react';

function App() {
  const account = useAccount()
  const { connectors, connect, status, error } = useConnect()
  const { disconnect } = useDisconnect()
  const { signMessageAsync } = useSignMessage()
  const message = `
packtpub.com wants you to sign in with your Ethereum account:
$address

I accept the PacktPub Terms of Service: https://www.packtpub.com/en-us/help/terms-and-conditions

URI: http://127.0.0.1:8000/token
Version: 1
Chain ID: 1
Nonce: $nonce
Issued At: $time
Resources:
- https://github.com/PacktPublishing/Hands-On-Blockchain-for-Python-Developers--2nd-Edition
`;

  const [nonce, setNonce] = useState('')
  const [nonceTime, setNonceTime] = useState('')
  const [token, setToken] = useState('')
  const [signature, setSignature] = useState('')
  const [profile, setProfile] = useState('')
  const [content, setContent] = useState('')
  const fetchNonce = async () => {
    try {
      const address = account.addresses[0]
      const response = await fetch(`http://localhost:8000/nonce/${address}`,
                                   {method: 'GET',
                                    headers: {'Content-Type': 'application/json'},
                                   })
      const nonceData = await response.json()
      const nonceValue = nonceData.nonce
      const nonceTimeValue = nonceData.nonce_time

      setNonce(nonceValue)
      setNonceTime(nonceTimeValue)
    } catch (error) {
      console.error('Error fetching nonce:', error)
    }
  };


  return (
    <>
      <div>
        <h2>Account</h2>

        <div>
          status: {account.status}
          <br />
          addresses: {JSON.stringify(account.addresses)}
          <br />
          chainId: {account.chainId}
        </div>

        {account.status === 'connected' && (
          <button type="button" onClick={() => disconnect()}>
            Disconnect
          </button>
        )}
      </div>

      <div>
        <h2>Connect</h2>
        {connectors.map((connector) => (
          <button
            key={connector.uid}
            onClick={() => connect({ connector })}
            type="button"
          >
            {connector.name}
          </button>
        ))}
        <div>{status}</div>
        <div>{error?.message}</div>
      </div>

      <div>
        <h2>Nonce</h2>
          <button
            onClick={() => fetchNonce()}
            type="button"
          >
            Get Nonce
          </button>
        <div>Nonce: {nonce}</div>
      </div>

      <div>
        <h2>Sign Message</h2>
        <button type="button"
                onClick={async () => {
                         const address = account.addresses[0]
                         const finalMessage = message.replace(/\$address/g, address)
                                                     .replace(/\$nonce/g, nonce)
                                                     .replace(/\$time/g, nonceTime)
                         const signedMessage = await signMessageAsync({ message: finalMessage })
                         setSignature(signedMessage)
                         const tokenRes = await fetch('http://localhost:8000/token', {
                                                       headers: {'Content-Type': 'application/json'},
                                                       method: 'POST',
                                                       body: JSON.stringify({ address, signature: signedMessage })
                                                 });
                         const tokenDict = await tokenRes.json()
                         setToken(tokenDict["access_token"])
                }}>
          Sign message
        </button>
        <div>Signature: {signature}</div>
        <div>Access Token: {token}</div>
      </div>

      <div>
        <h2>Profile</h2>
          <button
            onClick={async () => {
                         const meRes = await fetch('http://localhost:8000/me', {
                                                   headers: {'Content-Type': 'application/json',
                                                             'Authorization': `Bearer ${token}`,},
                                                   method: 'GET'})
                         const me = await meRes.json()
                         setProfile(JSON.stringify(me))
            }}
            type="button"
          >
            Get Profile
          </button>
        <div>Profile: {profile}</div>
      </div>

      <div>
        <h2>Content</h2>
          <button
            onClick={async () => {
                         const contentRes = await fetch('http://localhost:8000/content', {
                                                   headers: {'Content-Type': 'application/json',
                                                             'Authorization': `Bearer ${token}`,},
                                                   method: 'GET'})
                         const contentValue = await contentRes.json()
                         setContent(contentValue["content"])
            }}
            type="button"
          >
            Read Content
          </button>
        <div>Content: {content}</div>
      </div>
    </>
  )
}

export default App
