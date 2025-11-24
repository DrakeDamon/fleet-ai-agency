import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Script from 'next/script'
import './globals.css'
import Header from '../components/Header'
import Footer from '../components/Footer'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Fleet Clarity | AI-Powered Fleet Audits',
  description: 'Stop bleeding profit to breakdowns and fraud. Specialized AI diagnostics for fleets with 10-100 trucks.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <Script
          src="https://app.termly.io/resource-blocker/8e2bffdc-c7a1-4ba1-9655-e4be2242744c?autoBlock=on"
          strategy="beforeInteractive"
        />
      </head>
      <body className={inter.className}>
        <Header />
        {children}
        <Footer />
      </body>
    </html>
  )
}
