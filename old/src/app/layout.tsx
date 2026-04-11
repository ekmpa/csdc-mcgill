import type { Metadata } from "next";
import ThemeSwitcher from "@/components/theme-switcher";
import "./globals.css";

export const metadata: Metadata = {
  title: "McGill CSDC — Centre for the Study of Democratic Citizenship",
  description: "Research program at McGill CSDC focused on trust, democratic participation, and inclusion."
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html:
              "(function(){var t='default';try{t=localStorage.getItem('csdc-theme')||t;}catch(e){}var m=document.cookie.match(/(?:^|; )csdc-theme=([^;]+)/);if(m&&m[1]){t=decodeURIComponent(m[1]);}document.documentElement.setAttribute('data-theme',t);document.body&&document.body.setAttribute('data-theme',t);})();"
          }}
        />
      </head>
      <body suppressHydrationWarning>
        <header className="bg-mcgillDark text-white sticky top-0 z-50 border-b-4 border-mcgillRed">
          <nav className="max-w-6xl mx-auto px-4 py-3 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
            <div>
              <h1 className="text-lg font-bold tracking-wide">McGill CSDC</h1>
              <p className="text-xs text-gray-300">Centre for the Study of Democratic Citizenship</p>
            </div>
            <div className="flex flex-col items-start gap-2 md:items-end">
              <ul className="flex flex-wrap gap-x-5 gap-y-2 text-sm font-medium">
                <li><a href="/" className="hover:text-mcgillRed transition">Home</a></li>
                <li><a href="/about" className="hover:text-mcgillRed transition">About</a></li>
                <li><a href="/people" className="hover:text-mcgillRed transition">Team</a></li>
                <li><a href="/research" className="hover:text-mcgillRed transition">Research</a></li>
                <li><a href="/events" className="hover:text-mcgillRed transition">Events</a></li>
                <li><a href="/announcements" className="hover:text-mcgillRed transition">Opportunities</a></li>
              </ul>
              <ThemeSwitcher />
            </div>
          </nav>
        </header>
        <main className="min-h-screen">
          {children}
        </main>
        <footer className="bg-mcgillDark text-white mt-16 border-t-4 border-mcgillRed">
          <div className="max-w-6xl mx-auto px-4 py-12">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-8">
              <div>
                <h4 className="font-bold text-mcgillRed mb-2">McGill CSDC</h4>
                <p className="text-sm text-gray-300">Research team on trust, inclusion, and democratic citizenship.</p>
              </div>
              <div>
                <h4 className="font-bold text-mcgillRed mb-2">Quick Links</h4>
                <ul className="text-sm text-gray-300 space-y-1">
                  <li><a href="/#" className="hover:text-mcgillRed transition">Mission & Values</a></li>
                  <li><a href="/events" className="hover:text-mcgillRed transition">Events Calendar</a></li>
                  <li><a href="/announcements" className="hover:text-mcgillRed transition">Funding Opportunities</a></li>
                </ul>
              </div>
              <div className="flex flex-col justify-start">
                <div>
                  <h4 className="font-bold text-mcgillRed mb-2">Contact</h4>
                  <p className="text-sm text-gray-300">McGill University<br />Montréal, Quebec, Canada<br /><a href="mailto:info@mcgill-csdc.ca" className="hover:text-mcgillRed transition">info@mcgill-csdc.ca</a></p>
                </div>
              </div>
              <div className="flex items-center justify-start md:justify-end lg:self-center">
                <a href="/staff/login" className="text-mcgillRed hover:text-red-400 font-semibold text-sm transition">
                  Staff Login →
                </a>
              </div>
            </div>
            <div className="border-t border-gray-700 pt-6 text-sm text-gray-400 text-center">
              <p>&copy; 2026 McGill Centre for the Study of Democratic Citizenship. Part of the national CSDC network.</p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
