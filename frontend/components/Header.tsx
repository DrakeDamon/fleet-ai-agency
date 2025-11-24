import Image from "next/image";
import Link from "next/link";

export default function Header() {
  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
            <Image
                src="/logos/fleet logo.png"
                alt="Fleet Clarity"
                width={180}
                height={50}
                className="object-contain"
                priority
            />
        </Link>
        
        <div className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-600">
            <span>Audit Process</span>
            <span>Case Studies</span>
            <span>FAQ</span>
        </div>
      </div>
    </header>
  );
}
