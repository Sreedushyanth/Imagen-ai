"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Upload, ImageIcon, Sparkles } from "lucide-react"
import { generateStoryImages } from "@/app/actions"
import { ImageUpload } from "./image-upload"
import { GeneratedResults } from "./generated-results"

interface GenerationResult {
  success: boolean
  images?: string[]
  error?: string
}

export function StoryMakerInterface() {
  const [faceImage, setFaceImage] = useState<File | null>(null)
  const [maskImage, setMaskImage] = useState<File | null>(null)
  const [prompt, setPrompt] = useState("")
  const [negativePrompt, setNegativePrompt] = useState(
    "bad quality, low resolution, NSFW, cartoonish, disfigured, broken limbs",
  )
  const [isGenerating, setIsGenerating] = useState(false)
  const [results, setResults] = useState<GenerationResult | null>(null)

  const handleGenerate = async () => {
    if (!faceImage || !prompt) {
      alert("Please upload a face image and enter a prompt")
      return
    }

    setIsGenerating(true)
    setResults(null)

    try {
      const formData = new FormData()
      formData.append("faceImage", faceImage)
      if (maskImage) {
        formData.append("maskImage", maskImage)
      }
      formData.append("prompt", prompt)
      formData.append("negativePrompt", negativePrompt)

      const result = await generateStoryImages(formData)
      setResults(result)
    } catch (error) {
      setResults({
        success: false,
        error: "Failed to generate images. Please try again.",
      })
    } finally {
      setIsGenerating(false)
    }
  }

  const examplePrompts = [
    "a person reading a book under a cherry blossom tree in Kyoto",
    "a person exploring a neon-lit cyberpunk city",
    "a person sitting on Mars in a futuristic space suit",
    "a person standing near the Eiffel Tower during sunset, wearing a scarf",
    "a person in traditional Japanese attire walking through a misty forest",
  ]

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Upload Section */}
      <div className="grid md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Upload className="w-5 h-5" />
              Face Image (Required)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ImageUpload onImageSelect={setFaceImage} selectedImage={faceImage} placeholder="Upload your face image" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ImageIcon className="w-5 h-5" />
              Mask Image (Optional)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ImageUpload
              onImageSelect={setMaskImage}
              selectedImage={maskImage}
              placeholder="Upload mask image (optional)"
            />
          </CardContent>
        </Card>
      </div>

      {/* Prompt Section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="w-5 h-5" />
            Story Prompt
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label htmlFor="prompt">Describe your story scene</Label>
            <Textarea
              id="prompt"
              placeholder="e.g., a person reading a book under a cherry blossom tree in Kyoto"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="min-h-[100px]"
            />
          </div>

          <div>
            <Label htmlFor="negative-prompt">Negative Prompt</Label>
            <Textarea
              id="negative-prompt"
              placeholder="What you don't want in the image"
              value={negativePrompt}
              onChange={(e) => setNegativePrompt(e.target.value)}
              className="min-h-[80px]"
            />
          </div>

          <div>
            <Label>Example Prompts (click to use)</Label>
            <div className="flex flex-wrap gap-2 mt-2">
              {examplePrompts.map((example, index) => (
                <Button key={index} variant="outline" size="sm" onClick={() => setPrompt(example)} className="text-xs">
                  {example.slice(0, 50)}...
                </Button>
              ))}
            </div>
          </div>

          <Button
            onClick={handleGenerate}
            disabled={isGenerating || !faceImage || !prompt}
            className="w-full"
            size="lg"
          >
            {isGenerating ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                Generating Story Images...
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4 mr-2" />
                Generate Story Images
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Results Section */}
      {results && <GeneratedResults results={results} />}
    </div>
  )
}
