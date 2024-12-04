import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import AIFrontiersArticles from './pages/Newsletters';
import { ArchiveList } from './pages/ArchiveList';
import { ThemeProvider } from './context/ThemeProvider';
import Redirect from './components/Redirect';

function App() {  
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<AIFrontiersArticles limit={20}/>} />
            <Route path="/articles" element={<AIFrontiersArticles limit={20}/>} />
            <Route path="/archive" element={<ArchiveList />} />
            <Route path="/feedback" element={<Redirect to="https://aicrafter.canny.io/feature-requests" />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;