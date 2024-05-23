import {
	DefaultKeyboardShortcutsDialog,
	DefaultKeyboardShortcutsDialogContent,
	DefaultToolbar,
	DefaultToolbarContent,
	TLComponents,
	TLUiOverrides,
	Tldraw,
	TldrawUiMenuItem,
	computed,
	track,
	useIsToolSelected,
	useTools,
} from 'tldraw'
import 'tldraw/tldraw.css'
import { SlideShapeTool } from '../modules/SlideShapeTool'
import { SlideShapeUtil } from '../modules/SlideShapeUtil'
import { SlidesPanel } from '../modules/SlidesPanel'
import '../modules/slides.css'
import { $currentSlide, getSlides, moveToSlide } from '../modules/useSlides'

const components: TLComponents = {
	HelperButtons: SlidesPanel,
	Minimap: null,
	Toolbar: (props) => {
		const tools = useTools()
		const isSlideSelected = useIsToolSelected(tools['slide'])
		return (
			<DefaultToolbar {...props}>
				<TldrawUiMenuItem {...tools['slide']} isSelected={isSlideSelected} />
				<DefaultToolbarContent />
			</DefaultToolbar>
		)
	},
	KeyboardShortcutsDialog: (props) => {
		const tools = useTools()
		return (
			<DefaultKeyboardShortcutsDialog {...props}>
				<TldrawUiMenuItem {...tools['slide']} />
				<DefaultKeyboardShortcutsDialogContent />
			</DefaultKeyboardShortcutsDialog>
		)
	},
}

const overrides: TLUiOverrides = {
	actions(editor, actions) {
		const $slides = computed('slides', () => getSlides(editor))
		return {
			...actions,
			'next-slide': {
				id: 'next-slide',
				label: 'Next slide',
				kbd: 'right',
				onSelect() {
					const slides = $slides.get()
					const currentSlide = $currentSlide.get()
					const index = slides.findIndex((s) => s.id === currentSlide?.id)
					const nextSlide = slides[index + 1] ?? currentSlide ?? slides[0]
					if (nextSlide) {
						editor.stopCameraAnimation()
						moveToSlide(editor, nextSlide)
					}
				},
			},
			'previous-slide': {
				id: 'previous-slide',
				label: 'Previous slide',
				kbd: 'left',
				onSelect() {
					const slides = $slides.get()
					const currentSlide = $currentSlide.get()
					const index = slides.findIndex((s) => s.id === currentSlide?.id)
					const previousSlide = slides[index - 1] ?? currentSlide ?? slides[slides.length - 1]
					if (previousSlide) {
						editor.stopCameraAnimation()
						moveToSlide(editor, previousSlide)
					}
				},
			},
		}
	},
	tools(editor, tools) {
		tools.slide = {
			id: 'slide',
			icon: 'group',
			label: 'Slide',
			kbd: 's',
			onSelect: () => editor.setCurrentTool('slide'),
		}
		return tools
	},
}

const App = track(() => {
	return (
		<div style={{ width: '100%', height: '93%', position: 'fixed', top: '75px' }}>
			<Tldraw
				persistenceKey="slideshow-persistence-key"
				shapeUtils={[SlideShapeUtil]}
				tools={[SlideShapeTool]}
				components={components}
				overrides={overrides}
			/>
		</div>
	)
})

export default App