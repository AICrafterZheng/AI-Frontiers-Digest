import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import AIFrontiersArticles from './pages/Newsletters';
import { ArchiveList } from './pages/ArchiveList';
import AudioPlaylist from './pages/AudioPlaylist';
import { ThemeProvider } from './context/ThemeProvider';

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<AIFrontiersArticles limit={20}/>} />
            <Route path="/articles" element={<AIFrontiersArticles limit={20}/>} />
            <Route path="/archive" element={<ArchiveList />} />
            <Route path="/playlist" element={<AudioPlaylist />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;