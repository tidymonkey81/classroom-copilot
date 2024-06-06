import {
  DefaultKeyboardShortcutsDialog,
  DefaultKeyboardShortcutsDialogContent,
  DefaultMainMenu,
  DefaultMainMenuContent,
  DefaultToolbar,
  DefaultToolbarContent,
  TLComponents,
  TLUiOverrides,
  Tldraw,
  TldrawUiMenuItem,
  TldrawUiMenuGroup,
  computed,
  track,
  useIsToolSelected,
  useTools,
  DefaultPageMenu,
  createTLStore, // Added this import
} from 'tldraw';
import 'tldraw/tldraw.css';
import { SlideShapeTool } from './utils/slides/SlideShapeTool';
import { SlideShapeUtil } from './utils/slides/SlideShapeUtil';
import { SlidesPanel } from './utils/slides/SlidesPanel';
import './utils/slides/slides.css';
import { $currentSlide, getSlides, moveToSlide } from './utils/slides/useSlides';
import { useRef, useState } from 'react';

function CustomPageMenu() {
  return (
    <div style={{ transform: 'rotate(3.14rad)', backgroundColor: 'thistle' }}>
      <DefaultPageMenu />
    </div>
  );
}

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
          icon="folder_open"
          onSelect={onLoad}
        />
      </TldrawUiMenuGroup>
      <DefaultMainMenuContent />
    </DefaultMainMenu>
  );
}

const overrides: TLUiOverrides = {
  actions(editor, actions) {
    const $slides = computed('slides', () => getSlides(editor));
    return {
      ...actions,
      'next-slide': {
        id: 'next-slide',
        label: 'Next slide',
        kbd: 'right',
        onSelect() {
          const slides = $slides.get();
          const currentSlide = $currentSlide.get();
          const index = slides.findIndex((s) => s.id === currentSlide?.id);
          const nextSlide = slides[index + 1] ?? currentSlide ?? slides[0];
          if (nextSlide) {
            editor.stopCameraAnimation();
            moveToSlide(editor, nextSlide);
          }
        },
      },
      'previous-slide': {
        id: 'previous-slide',
        label: 'Previous slide',
        kbd: 'left',
        onSelect() {
          const slides = $slides.get();
          const currentSlide = $currentSlide.get();
          const index = slides.findIndex((s) => s.id === currentSlide?.id);
          const previousSlide = slides[index - 1] ?? currentSlide ?? slides[slides.length - 1];
          if (previousSlide) {
            editor.stopCameraAnimation();
            moveToSlide(editor, previousSlide);
          }
        },
      },
    };
  },
  tools(editor, tools) {
    tools.slide = {
      id: 'slide',
      icon: 'group',
      label: 'Slide',
      kbd: 's',
      onSelect: () => editor.setCurrentTool('slide'),
    };
    return tools;
  },
};

const SlidesExample = track(() => {
  const fileInputRef = useRef(null);
  const [store, setStore] = useState(() => createTLStore({
    shapeUtils: [SlideShapeUtil],
  }));

  const handleSaveCopy = () => {
    const snapshot = store.getSnapshot();
    const stringified = JSON.stringify(snapshot);
    const blob = new Blob([stringified], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'drawing.tldr';
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleLoadFile = () => {
    fileInputRef.current.click();
  };

  const components: TLComponents = {
    MainMenu: (props) => <CustomMainMenu {...props} onSave={handleSaveCopy} onLoad={handleLoadFile} />,
    HelperButtons: SlidesPanel,
    Minimap: null,
    Toolbar: (props) => {
      const tools = useTools();
      const isSlideSelected = useIsToolSelected(tools['slide']);
      return (
        <DefaultToolbar {...props}>
          <TldrawUiMenuItem {...tools['slide']} isSelected={isSlideSelected} />
          <DefaultToolbarContent />
        </DefaultToolbar>
      );
    },
    KeyboardShortcutsDialog: (props) => {
      const tools = useTools();
      return (
        <DefaultKeyboardShortcutsDialog {...props}>
          <TldrawUiMenuItem {...tools['slide']} />
          <DefaultKeyboardShortcutsDialogContent />
        </DefaultKeyboardShortcutsDialog>
      );
    },
    PageMenu: CustomPageMenu,
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target.result;
        const snapshot = JSON.parse(content);
        store.loadSnapshot(snapshot);
      };
      reader.readAsText(file);
    }
  };

  return (
    <div style={{ display: 'flex', height: '100%' }}>
      <input
        type="file"
        accept=".tldr"
        style={{ display: 'none' }}
        ref={fileInputRef}
        onChange={handleFileChange}
      />
      <Tldraw
        persistenceKey="slideshow_example"
        shapeUtils={[SlideShapeUtil]}
        tools={[SlideShapeTool]}
        components={components}
        overrides={overrides}
      />
    </div>
  );
});

export default SlidesExample;
