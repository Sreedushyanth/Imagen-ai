"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Download, AlertCircle, CheckCircle } from "lucide-react"
import Image from "next/image"

interface GenerationResult {
  success: boolean
  images?: string[]
  error?: string
}

interface GeneratedResultsProps {
  results: GenerationResult
}

export function GeneratedResults({ results }: GeneratedResultsProps) {
  const handleDownload = async (imageUrl: string, index: number) => {
    try {
      const response = await fetch(imageUrl)
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `story-image-${index + 1}.jpg`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error("Download failed:", error)
    }
  }

  const handleDownloadAll = async () => {
    if (results.images) {
      for (let i = 0; i < results.images.length; i++) {
        await handleDownload(results.images[i], i)
        // Add small delay between downloads
        await new Promise((resolve) => setTimeout(resolve, 500))
      }
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          {results.success ? (
            <>
              <CheckCircle className="w-5 h-5 text-green-500" />
              Generated Story Images
            </>
          ) : (
            <>
              <AlertCircle className="w-5 h-5 text-red-500" />
              Generation Failed
            </>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {results.success && results.images ? (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <p className="text-sm text-gray-600">Generated {results.images.length} story images</p>
              <Button onClick={handleDownloadAll} variant="outline">
                <Download className="w-4 h-4 mr-2" />
                Download All
              </Button>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              {results.images.map((imageUrl, index) => (
                <div key={index} className="relative group">
                  <div className="relative w-full h-64 rounded-lg overflow-hidden border">
                    <Image
                      src={imageUrl || "/placeholder.svg"}
                      alt={`Generated story image ${index + 1}`}
                      fill
                      className="object-cover"
                    />
                  </div>
                  <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-200 rounded-lg flex items-center justify-center">
                    <Button
                      onClick={() => handleDownload(imageUrl, index)}
                      className="opacity-0 group-hover:opacity-100 transition-opacity"
                      size="sm"
                    >
                      <Download className="w-4 h-4 mr-2" />
                      Download
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="text-center py-8">
            <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
            <p className="text-red-600 font-medium">Generation Failed</p>
            <p className="text-sm text-gray-600 mt-2">{results.error || "An unexpected error occurred"}</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
