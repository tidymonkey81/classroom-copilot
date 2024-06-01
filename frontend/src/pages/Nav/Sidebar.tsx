import { Link } from 'react-router-dom';

const Sidebar = () => (
  <aside className="w-64 bg-gray-800 text-white p-4">
    <nav>
      <Link to="/labs/slides" className="block py-2">Slides</Link>
      <Link to="/labs/draw-file" className="block py-2">File</Link>
      <Link to="/labs/propagator" className="block py-2">Propagator</Link>
    </nav>
  </aside>
);

export default Sidebar;