import '@/styles/globals.css'
//import 'bootstrap/dist/css/bootsrap.min.css'
import * as firebase from 'firebase/app'
import 'firebase/database'

const firebaseConfig ={
  apiKey: "AIzaSyBgVy7prDmaKqjtyFs30eCnJbolsU4oXqQ",
  authDomain: "makeohio2023.firebaseapp.com",
  databaseURL: "https://makeohio2023-default-rtdb.firebaseio.com",
  projectId: "makeohio2023",
  storageBucket: "makeohio2023.appspot.com",
  messagingSenderId: "223873348661",
  appId: "1:223873348661:web:b827f3ce6ef0c4fd4f6d7c",
  measurementId: "G-4HBVC9W6E7"
}

firebase.initializeApp(firebaseConfig)

export default function App({ Component, pageProps }) {
  return <Component {...pageProps} />
}
