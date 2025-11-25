import Image from "next/image";
import Link from "next/link";

export default function Header() {
  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div className="w-full px-6 h-16 flex items-center justify-between">
        {/* <Link href="/" className="flex items-center gap-2">
            <div className="relative h-14 w-48">
                <Image
                    src="/logos/fleet logo.png"
                    alt="Fleet Clarity"
                    fill
                    className="object-contain object-left"
                    sizes="(max-width: 768px) 100vw, 200px"
                    priority
                />
            </div>
        </Link> */}
        
        <div className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-600">
            <Link href="/" className="hover:text-slate-900 transition-colors">Home</Link>
            <Link href="/audit-process" className="hover:text-slate-900 transition-colors">Audit Process</Link>
            <Link href="/faq" className="hover:text-slate-900 transition-colors">FAQ</Link>
        </div>
      </div>
    </header>
  );
}
