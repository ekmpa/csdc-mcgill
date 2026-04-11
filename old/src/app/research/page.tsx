export default function ResearchPage() {
  const researchAreas = [
    {
      title: "Social Trust and Cohesion",
      description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
      projects: ["Lorem ipsum dolor", "Consectetur adipiscing elit"]
    },
    {
      title: "Diversity, Immigration, and Belonging",
      description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
      projects: ["Sed do eiusmod tempor", "Incididunt ut labore"]
    },
    {
      title: "Democratic Participation and Representation",
      description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
      projects: ["Et dolore magna aliqua", "Ut enim ad minim"]
    },
    {
      title: "Comparative Public Opinion",
      description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
      projects: ["Veniam quis nostrud", "Exercitation ullamco"]
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-white">
      <div className="max-w-6xl mx-auto px-4 py-16">
        <h1 className="text-3xl md:text-4xl font-bold text-mcgillRed mb-2">Our Research</h1>
        <p className="text-lg text-gray-600 mb-12 max-w-3xl">
          Our team conducts empirical, comparative research on trust, democratic participation, and inclusion. Our work combines advanced quantitative methods with policy-relevant scholarship.
        </p>

        {/* Research Areas */}
        <section className="mb-16">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-8">Research Areas</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {researchAreas.map((area, idx) => (
              <div key={idx} className="bg-white border border-gray-200 rounded-lg shadow-sm p-6 hover:shadow-md transition">
                <h3 className="text-xl font-bold text-mcgillRed mb-3">{area.title}</h3>
                <p className="text-gray-700 mb-4">{area.description}</p>
                <div>
                  <p className="text-xs font-bold text-gray-600 uppercase mb-2">Current Projects</p>
                  <ul className="text-sm text-gray-600 space-y-1">
                    {area.projects.map((proj, i) => (
                      <li key={i} className="flex items-center gap-2">
                        <span className="w-2 h-2 bg-mcgillRed rounded-full"></span> {proj}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Publications */}
        <section className="mb-16">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-6">Recent Publications</h2>
          <div className="space-y-4">
            <div className="bg-white border-l-4 border-mcgillRed rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-2">
                "Trust, Diversity, and Democratic Stability in Canada"
              </h3>
              <p className="text-gray-600 mb-2">
                <em>Canadian Journal of Political Science</em>, 2025. Stolle, D., Berger, S., & Rahman, N.
              </p>
              <a href="#" className="text-mcgillRed hover:text-red-700 font-semibold text-sm">Read paper →</a>
            </div>

            <div className="bg-white border-l-4 border-mcgillRed rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-2">
                "Belonging and Participation Among New Canadians"
              </h3>
              <p className="text-gray-600 mb-2">
                <em>Citizenship Studies</em>, 2024. Rahman, N. & Stolle, D.
              </p>
              <a href="#" className="text-mcgillRed hover:text-red-700 font-semibold text-sm">Read paper →</a>
            </div>
          </div>
        </section>

        {/* Datasets */}
        <section className="bg-mcgillDark text-white rounded-lg p-8">
          <h2 className="text-2xl font-bold mb-4 text-mcgillRed">Open Data & Datasets</h2>
          <p className="text-gray-200 mb-6">
            We believe in open science and make many of our datasets publicly available for researchers and the public.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <a href="#" className="bg-white/10 hover:bg-mcgillRed p-4 rounded-lg transition border border-white/20">
              <h3 className="text-lg font-bold text-mcgillRed mb-2">Canadian Trust and Democracy Panel</h3>
              <p className="text-gray-300 text-sm">Longitudinal panel on trust, participation, and democratic attitudes across provinces (2015-2026).</p>
            </a>
            <a href="#" className="bg-white/10 hover:bg-mcgillRed p-4 rounded-lg transition border border-white/20">
              <h3 className="text-lg font-bold text-mcgillRed mb-2">Montreal Diversity and Belonging Survey</h3>
              <p className="text-gray-300 text-sm">City-level dataset on integration, local trust, and political efficacy in diverse neighborhoods.</p>
            </a>
          </div>
        </section>
      </div>
    </div>
  );
}
