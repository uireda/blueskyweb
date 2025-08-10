import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Blue Sky Tourism - Votre Agence de Voyages de Confiance",
  description:
    "Découvrez le monde avec Blue Sky Tourism. Des années d'expérience pour vous offrir les voyages de vos rêves. Destinations, clubs, circuits et voyages sur mesure.",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fr">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
