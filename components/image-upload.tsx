"use client"

import type React from "react"

import { useRef, useState } from "react"
import { Button } from "@/components/ui/button"
import { Upload, X } from "lucide-react"
import Image from "next/image"

interface ImageUploadProps {
  onImageSelect: (file: File | null) => void
  selectedImage: File | null
  placeholder: string
}

export function ImageUpload({ onImageSelect, selectedImage, placeholder }: ImageUploadProps) {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      onImageSelect(file)
      const url = URL.createObjectURL(file)
      setPreviewUrl(url)
    }
  }

  const handleRemove = () => {
    onImageSelect(null)
    setPreviewUrl(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  return (
    <div className="space-y-4">
      <input ref={fileInputRef} type="file" accept="image/*" onChange={handleFileSelect} className="hidden" />

      {previewUrl ? (
        <div className="relative">
          <div className="relative w-full h-48 rounded-lg overflow-hidden border-2 border-dashed border-gray-300">
            <Image src={previewUrl || "/placeholder.svg"} alt="Preview" fill className="object-cover" />
          </div>
          <Button onClick={handleRemove} variant="destructive" size="sm" className="absolute top-2 right-2">
            <X className="w-4 h-4" />
          </Button>
        </div>
      ) : (
        <div
          onClick={() => fileInputRef.current?.click()}
          className="w-full h-48 border-2 border-dashed border-gray-300 rounded-lg flex flex-col items-center justify-center cursor-pointer hover:border-gray-400 transition-colors"
        >
          <Upload className="w-8 h-8 text-gray-400 mb-2" />
          <p className="text-sm text-gray-500 text-center">{placeholder}</p>
          <p className="text-xs text-gray-400 mt-1">Click to browse files</p>
        </div>
      )}
    </div>
  )
}
