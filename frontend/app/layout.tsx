import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Script from 'next/script'
import { GoogleTagManager } from '@next/third-parties/google'
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
          src={process.env.NEXT_PUBLIC_TERMLY_URL}
          strategy="beforeInteractive"
        />
      </head>
      <body className={inter.className}>
        <Header />
        {children}
        <Footer />
        <GoogleTagManager gtmId={process.env.NEXT_PUBLIC_GTM_ID || ""} />
      </body>
    </html>
  )
}
