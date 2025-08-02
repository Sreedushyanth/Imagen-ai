import { StoryMakerInterface } from "@/components/story-maker-interface"

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">AI StoryMaker</h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Transform your photos into creative AI-generated story scenes using advanced Stable Diffusion XL technology
          </p>
        </div>
        <StoryMakerInterface />
      </div>
    </div>
  )
}
