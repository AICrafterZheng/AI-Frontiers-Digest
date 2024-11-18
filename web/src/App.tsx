import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import AIFrontiersArticles from './pages/Newsletters';
import { ArchiveList } from './pages/ArchiveList';
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<AIFrontiersArticles limit={20} date={new Date().toISOString()}/>} />
          <Route path="/articles" element={<AIFrontiersArticles limit={20}/>} />
          <Route path="/archive" element={<ArchiveList />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;