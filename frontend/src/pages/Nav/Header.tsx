import { Link } from 'react-router-dom';

const Header = () => (
    <header className="bg-blue-500 p-4 text-white">
        <nav>
            <Link to="/" className="mr-4">Home</Link>
            <Link to="/admin" className="mr-4">Admin</Link>
            <Link to="/llm-tools" className="mr-4">LLM Tools</Link>
            <Link to="/transcription-tools" className="mr-4">Transcription Tools</Link>
            <Link to="/flow" className="mr-4">Flow</Link>
            <Link to="/draw" className="mr-4">Draw</Link>
        </nav>
    </header>
);

export default Header;