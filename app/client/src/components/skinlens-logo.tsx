interface LogoProps {
  size?: number;
  className?: string;
}

export function SkinLensIcon({ size = 18, className = "" }: LogoProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="2" fill="none" />
      <line x1="16.5" y1="16.5" x2="21" y2="21" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
      <path d="M9 9.5C9.5 8.5 10.5 8 11.5 8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <circle cx="11" cy="11" r="3" stroke="currentColor" strokeWidth="1.2" strokeDasharray="2 2" fill="none" />
    </svg>
  );
}

export function SkinLensLogo({ size = 32 }: { size?: number }) {
  return (
    <div
      className="rounded-lg bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center"
      style={{ width: size, height: size }}
    >
      <SkinLensIcon size={size * 0.56} className="text-white" />
    </div>
  );
}
