import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar = ({ isOpen, setIsOpen }) => {
  const toggleSidebar = () => setIsOpen(!isOpen);

  return (
    <aside className={`bg-gray-800 text-white transition-all duration-300 ${isOpen ? 'w-32' : 'w-0'} h-full relative`}>
      <button 
        onClick={toggleSidebar} 
        className={`text-white absolute top-1/2 right-0 transform translate-x-full -translate-y-1/2 ${isOpen ? 'bg-gray-800' : 'bg-gray-600'}`}
        style={{ width: '32px', height: '32px', zIndex: 1000 }}
      >
        {isOpen ? '←' : '→'}
      </button>
      <div className={`pt-8 ${isOpen ? 'block' : 'hidden'}`}>
        <nav style={{ paddingLeft: '15px' }}>
          <Link to="/labs" className="block py-2">Labs</Link>
          <Link to="/labs/slides" className="block py-2">Slides</Link>
          <Link to="/labs/draw-file" className="block py-2">File</Link>
          <Link to="/labs/propagator" className="block py-2">Propagator</Link>
        </nav>
      </div>
    </aside>
  );
};

export default Sidebar;


