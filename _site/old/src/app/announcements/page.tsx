export default function AnnouncementsPage() {
  const mockAnnouncements = [
    {
      id: "1",
      title: "Call for Graduate Affiliates: Research Team 2026 Cohort",
      kind: "opportunity",
      deadline: "April 30, 2026",
      summary: "Applications are open for graduate students interested in trust, participation, and diversity research. Affiliates receive mentorship, data training, and project support.",
      audience: "Graduate Students"
    },
    {
      id: "2",
      title: "Postdoctoral Position in Democratic Citizenship Research",
      kind: "opportunity",
      deadline: "May 20, 2026",
      summary: "The research team seeks a postdoctoral fellow with strengths in quantitative political behavior, public opinion, or migration and inclusion studies.",
      audience: "Postdoctoral Researchers"
    },
    {
      id: "3",
      title: "Methods Working Group Launch",
      kind: "resource",
      deadline: "Ongoing",
      summary: "Monthly workshops on survey design, causal inference, and comparative datasets led by team members and invited experts.",
      audience: "Team Members and Affiliates"
    },
    {
      id: "4",
      title: "New Publication from the Research Team",
      kind: "news",
      deadline: "Published",
      summary: "A new article on trust and democratic resilience has been published, highlighting comparative evidence from Canadian and European survey data.",
      audience: "Public and Academic Partners"
    }
  ];

  const badgeColor = (kind: string) => {
    switch (kind) {
      case "opportunity":
        return "bg-emerald-100 text-emerald-900";
      case "resource":
        return "bg-blue-100 text-blue-900";
      case "news":
        return "bg-purple-100 text-purple-900";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-white">
      <div className="max-w-6xl mx-auto px-4 py-16">
        <h1 className="text-3xl md:text-4xl font-bold text-mcgillRed mb-2">Funding & Opportunities</h1>
        <p className="text-lg text-gray-600 mb-12">
          News, positions, and research opportunities from the McGill CSDC research team.
        </p>

        <div className="space-y-6">
          {mockAnnouncements.map((announcement) => (
            <div key={announcement.id} className="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition p-6">
              <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 sm:gap-4 mb-4">
                <h2 className="text-lg md:text-xl font-bold text-gray-900 flex-1">{announcement.title}</h2>
                <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase whitespace-nowrap ${badgeColor(announcement.kind)}`}>
                  {announcement.kind === "opportunity" ? "Funding" : announcement.kind === "resource" ? "Resource" : "News"}
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 mb-4 text-sm text-gray-700">
                <div>
                  <p className="text-xs text-gray-500 uppercase font-bold mb-1">Deadline</p>
                  <p className="text-sm font-semibold">{announcement.deadline}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 uppercase font-bold mb-1">Target Audience</p>
                  <p className="text-sm font-semibold">{announcement.audience}</p>
                </div>
              </div>

              <p className="text-gray-700 leading-relaxed mb-4">{announcement.summary}</p>
              <a href="#" className="text-mcgillRed font-semibold hover:text-red-700 transition inline-block">
                Learn more & apply →
              </a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
