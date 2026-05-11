export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-white">
      {/* Hero */}
      <section className="bg-gradient-to-b from-white via-gray-50 to-gray-100 py-16 md:py-20">
        <div className="max-w-6xl mx-auto px-4">
          {/* Logo / Branding */}
          <div className="mb-8">
            <p className="text-sm md:text-base font-semibold mb-2">
              <span className="text-mcgillRed">CSDC / </span>
              <span className="text-cecd">CÉCD</span>
            </p>
            <h1 className="text-3xl md:text-4xl font-bold text-mcgillDark mb-2 leading-tight">
              Centre for the Study of Democratic Citizenship
            </h1>
            <h2 className="text-2xl md:text-3xl font-bold text-gray-500 leading-tight">
              Centre pour L'Étude de la Citoyenneté Démocratique
            </h2>
          </div>

          <p className="text-lg text-gray-700 max-w-3xl mb-10 leading-relaxed mt-8">
            The McGill CSDC team studies democratic citizenship, justice and political behaviors. We combine survey research, comparative analysis, and public engagement to understand how democracy works in everyday life.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
            <a href="/research" className="btn-primary inline-block text-center">Our Research</a>
            <a href="/events" className="btn-secondary inline-block text-center">View Upcoming Events</a>
          </div>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 py-16">

      {/* Featured Event */}
      <section className="mb-16 bg-white border-l-4 border-mcgillRed shadow-sm rounded p-6">
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-5">
          <div className="flex-1">
            <span className="text-xs font-bold text-mcgillRed uppercase tracking-wide mb-2 block">Featured Seminar</span>
            <h2 className="text-2xl font-bold text-gray-900 mb-3">Trust, Diversity, and Democratic Resilience</h2>
            <p className="text-gray-700 mb-2"><strong>Date:</strong> Thursday, April 9, 2:00 PM ET</p>
            <p className="text-gray-700 mb-4"><strong>Location:</strong> Leacock Building, Room 232</p>
            <a href="/events" className="text-mcgillRed font-semibold hover:text-red-700 transition">View all seminars →</a>
          </div>
          <div className="text-left sm:text-right sm:ml-6">
            <div className="inline-block bg-mcgillRed text-white px-4 py-6 rounded text-center">
              <p className="text-3xl font-bold">09</p>
              <p className="text-sm">April</p>
            </div>
          </div>
        </div>
      </section>

      {/* Research Pillars */}
      <section className="mb-16">
        <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-8">Our Research Focus</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white border-t-4 border-mcgillRed p-6 rounded shadow-sm hover:shadow-md transition">
            <h3 className="text-lg font-bold text-mcgillRed mb-2">Social Trust</h3>
            <p className="text-gray-600 text-sm">How interpersonal trust forms, erodes, and influences civic and political life.</p>
          </div>
          <div className="bg-white border-t-4 border-mcgillRed p-6 rounded shadow-sm hover:shadow-md transition">
            <h3 className="text-lg font-bold text-mcgillRed mb-2">Diversity & Inclusion</h3>
            <p className="text-gray-600 text-sm">Investigating belonging, integration, and democratic inclusion in plural societies.</p>
          </div>
          <div className="bg-white border-t-4 border-mcgillRed p-6 rounded shadow-sm hover:shadow-md transition">
            <h3 className="text-lg font-bold text-mcgillRed mb-2">Democratic Participation</h3>
            <p className="text-gray-600 text-sm">Analyzing participation patterns, youth engagement, and inequality in representation.</p>
          </div>
          <div className="bg-white border-t-4 border-mcgillRed p-6 rounded shadow-sm hover:shadow-md transition">
            <h3 className="text-lg font-bold text-mcgillRed mb-2">Comparative Public Opinion</h3>
            <p className="text-gray-600 text-sm">Using cross-national data to track democratic attitudes over time.</p>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="bg-mcgillDark text-white rounded-lg p-6 md:p-12 mb-16">
        <h2 className="text-2xl font-bold mb-4">Get Involved</h2>
        <p className="text-gray-200 mb-6 max-w-2xl">Our team welcomes collaborators, graduate students, and partners from academia and civil society.</p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-6">
          <a href="/announcements" className="text-mcgillRed font-semibold hover:text-red-400 transition block">→ Funding & Grants</a>
          <a href="/events" className="text-mcgillRed font-semibold hover:text-red-400 transition block">→ Upcoming Events</a>
          <a href="/people" className="text-mcgillRed font-semibold hover:text-red-400 transition block">→ Our Team</a>
        </div>
      </section>

      {/* Quick Stats */}
      <section className="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-16 text-center">
        <div>
          <p className="text-4xl font-bold text-mcgillRed mb-2">25+</p>
          <p className="text-gray-600">Team Members & Affiliates</p>
        </div>
        <div>
          <p className="text-4xl font-bold text-mcgillRed mb-2">8</p>
          <p className="text-gray-600">International Partnerships</p>
        </div>
        <div>
          <p className="text-4xl font-bold text-mcgillRed mb-2">30+</p>
          <p className="text-gray-600">Talks & Workshops / Year</p>
        </div>
        <div>
          <p className="text-4xl font-bold text-mcgillRed mb-2">15+</p>
          <p className="text-gray-600">Major Publications / Year</p>
        </div>
      </section>
    </div>
    </div>
  );
}
