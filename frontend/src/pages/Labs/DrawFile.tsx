import React, { useRef } from 'react';
import {
  DefaultMainMenu,
  DefaultMainMenuContent,
  TLComponents,
  Tldraw,
  TldrawUiMenuGroup,
  TldrawUiMenuItem,
} from 'tldraw';
import 'tldraw/tldraw.css';

function CustomMainMenu({ onSave, onLoad }) {
  return (
    <DefaultMainMenu>
      <TldrawUiMenuGroup id="file">
        <TldrawUiMenuItem
          id="save"
          label="Save Copy"
          icon="save"
          readonlyOk
          onSelect={onSave}
        />
        <TldrawUiMenuItem
          id="load"
          label="Load File"
          icon="folder-open"
          readonlyOk
          onSelect={onLoad}
        />
      </TldrawUiMenuGroup>
      <DefaultMainMenuContent />
    </DefaultMainMenu>
  );
}

export default function CustomMainMenuExample() {
  const editorRef = useRef(null);
  const fileInputRef = useRef(null);

  const handleSaveCopy = () => {
    if (editorRef.current) {
      const snapshot = editorRef.current.store.getSnapshot();
      const stringified = JSON.stringify(snapshot);
      const blob = new Blob([stringified], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'drawing.tldr';
      a.click();
      URL.revokeObjectURL(url);
    }
  };

  const handleLoadFile = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target.result;
        const snapshot = JSON.parse(content);
        if (editorRef.current) {
          editorRef.current.store.setSnapshot(snapshot);
        }
      };
      reader.readAsText(file);
    }
  };

  const components = {
    MainMenu: (props) => <CustomMainMenu {...props} onSave={handleSaveCopy} onLoad={handleLoadFile} />,
  };

  return (
    <div style={{ display: 'flex', height: '100%' }}>
      <div style={{ flex: 1 }}>
        <input
          type="file"
          accept=".tldr"
          style={{ display: 'none' }}
          ref={fileInputRef}
          onChange={handleFileChange}
        />
        <Tldraw
          components={components}
          persistenceKey="draw-file-persistence-key-new"
          onMount={(editor) => {
            editorRef.current = editor;
          }}
        />
      </div>
    </div>
  );
}
