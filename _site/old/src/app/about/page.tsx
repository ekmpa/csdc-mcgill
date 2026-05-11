export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-white">
      <div className="max-w-6xl mx-auto px-4 py-16">
        <h1 className="text-3xl md:text-4xl font-bold text-mcgillRed mb-2">Mission</h1>
        <p className="text-lg text-gray-600 mb-12 max-w-3xl">
          The McGill node of the CSDC advances rigorous scholarship on trust, democratic participation, and social cohesion in Canada and globally.
        </p>

        {/* Mission */}
        <section className="mb-16">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-6">Our Mission</h2>
          <div className="about-box border-l-4 border-mcgillRed rounded-lg shadow-sm p-6 mb-6">
            <p className="text-gray-700 leading-relaxed text-lg">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            </p>
          </div>
        </section>

        {/* Values */}
        <section className="mb-16">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-6">Core Values</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="about-box border-t-4 border-mcgillRed rounded-lg shadow-sm p-6">
              <h3 className="text-xl font-bold text-mcgillRed mb-3">Inclusivity</h3>
              <p className="text-gray-700">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
            </div>
            <div className="about-box border-t-4 border-mcgillRed rounded-lg shadow-sm p-6">
              <h3 className="text-xl font-bold text-mcgillRed mb-3">Rigor</h3>
              <p className="text-gray-700">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
            </div>
            <div className="about-box border-t-4 border-mcgillRed rounded-lg shadow-sm p-6">
              <h3 className="text-xl font-bold text-mcgillRed mb-3">Impact</h3>
              <p className="text-gray-700">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
            </div>
            <div className="about-box border-t-4 border-mcgillRed rounded-lg shadow-sm p-6">
              <h3 className="text-xl font-bold text-mcgillRed mb-3">Collaboration</h3>
              <p className="text-gray-700">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
            </div>
          </div>
        </section>

        {/* History */}
        <section className="mb-16">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-6">History & Mission</h2>
          <p className="about-box text-gray-700 leading-relaxed mb-4 p-6 rounded-lg shadow-sm">
            The McGill CSDC has developed into a leading site for research on democratic citizenship. The team has expanded to include faculty, postdoctoral fellows, graduate researchers, and international collaborators.
          </p>
          <p className="about-box text-gray-700 leading-relaxed p-6 rounded-lg shadow-sm">
            Team projects are supported by major competitive grants and institutional partnerships. Alongside publishing in top journals, we prioritize student training, open data practices, and public-facing scholarship.
          </p>
        </section>

        {/* National Network */}
        <section className="bg-mcgillDark text-white rounded-lg p-8">
          <h2 className="text-2xl font-bold mb-4 text-mcgillRed">Part of the National CSDC Network</h2>
          <p className="text-gray-200 mb-6">
            The McGill CSDC is one of eight university nodes in the national Centre for the Study of Democratic Citizenship. Learn more about our partners and the broader network at <a href="https://csdc-cecd.ca" className="text-mcgillRed hover:text-red-400 underline">csdc-cecd.ca</a>.
          </p>
          <p className="text-gray-300 text-sm">
            Partner universities include: University of Montréal, Université Laval, University of Toronto, University of British Columbia, and others across Canada.
          </p>
        </section>
      </div>
    </div>
  );
}
