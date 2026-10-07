// 응모 수첩 · Firebase 연결 모듈
// 이 파일을 묶어서(esbuild) 저장소 맨 위의 fb.js를 만들어요. 화면 코드는 window.__fbLoaded로 이 기능들을 받아 써요.
//   npx esbuild tools/fb-entry.js --bundle --minify --format=iife --outfile=fb.js
import { initializeApp } from 'firebase/app';
import {
  getAuth, GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged,
} from 'firebase/auth';
import {
  initializeFirestore, persistentLocalCache, persistentMultipleTabManager,
  collection, doc, setDoc, deleteDoc, onSnapshot, writeBatch, getDocs,
} from 'firebase/firestore';

const firebaseConfig = {
  apiKey: 'AIzaSyBOUpM4JURMjnoQk8Ya4pG0BheQU3s0D3c',
  authDomain: 'eungmo.firebaseapp.com',
  projectId: 'eungmo',
  storageBucket: 'eungmo.firebasestorage.app',
  messagingSenderId: '340665645744',
  appId: '1:340665645744:web:f2826366c09091520d5975',
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// 인터넷이 잠깐 끊겨도 기기에 기록을 들고 있다가 다시 연결되면 저장해요
let db;
try {
  db = initializeFirestore(app, {
    localCache: persistentLocalCache({ tabManager: persistentMultipleTabManager() }),
    ignoreUndefinedProperties: true,
  });
} catch (e) {
  db = initializeFirestore(app, { ignoreUndefinedProperties: true });
}

const api = {
  auth, db, GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged,
  collection, doc, setDoc, deleteDoc, onSnapshot, writeBatch, getDocs,
};
if (typeof window.__fbLoaded === 'function') window.__fbLoaded(api);
else window.__fbApi = api;
