import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import AIFrontiersArticles from './pages/Newsletters';
import { ArchiveList } from './pages/ArchiveList';
import { ThemeProvider } from './context/ThemeProvider';
import Redirect from './components/Redirect';
import Newsletter from './pages/Newsletter';
import NotFound from './pages/NotFound';

function App() {  
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<AIFrontiersArticles/>} />
            <Route path="/articles" element={<AIFrontiersArticles/>} />
            <Route path="/archive" element={<ArchiveList />} />
            <Route path="/feedback" element={<Redirect to="https://aicrafter.canny.io/feature-requests" />} />
            <Route path="/news/:id" element={<Newsletter />} />
            <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}
export default App;