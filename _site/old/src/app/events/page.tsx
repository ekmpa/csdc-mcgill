export default function EventsPage() {
  const mockEvents = [
    {
      id: "1",
      title: "Trust, Diversity, and Democratic Resilience",
      date: "April 9, 2026",
      time: "2:00 PM – 3:30 PM ET",
      category: "Seminar",
      location: "Leacock Building, Room 232",
      speaker: "CSDC Research Team (McGill University)",
      description: "Opening seminar of the McGill CSDC research series on trust formation and democratic stability in diverse societies."
    },
    {
      id: "2",
      title: "Belonging and Political Inclusion in Montreal",
      date: "April 16, 2026",
      time: "1:00 PM – 2:30 PM ET",
      category: "Workshop",
      location: "Virtual (Zoom)",
      speaker: "Dr. Nadia Rahman (McGill CSDC)",
      description: "A methods workshop on measuring belonging, social trust, and civic participation among newcomer communities."
    },
    {
      id: "3",
      title: "Youth Participation After the Pandemic",
      date: "April 24, 2026",
      time: "10:00 AM – 11:30 AM ET",
      category: "Lecture",
      location: "Leacock Building, Room 429",
      speaker: "Maya Leclerc (Doctoral Researcher, McGill)",
      description: "New evidence on youth political efficacy, civic learning, and digital pathways into democratic participation."
    }
  ];

  return (
    <div className="events-page min-h-screen bg-gradient-to-br from-gray-50 to-white">
      <div className="max-w-6xl mx-auto px-4 py-16">
        <h1 className="text-3xl md:text-4xl font-bold text-mcgillRed mb-2">Seminars & Events</h1>
        <p className="text-lg text-gray-600 mb-12">
          Join our team for seminars, methods workshops, and public lectures on trust, inclusion, and democratic participation.
        </p>

        <div className="space-y-6">
          {mockEvents.map((event) => (
            <div key={event.id} className="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition p-6">
              <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-3">
                    <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide ${
                      event.category === "Seminar"
                        ? "bg-mcgillRed text-white"
                        : event.category === "Workshop"
                        ? "bg-amber-100 text-amber-900"
                        : "bg-blue-100 text-blue-900"
                    }`}>
                      {event.category}
                    </span>
                  </div>
                  <h2 className="text-xl md:text-2xl font-bold text-gray-900 mb-2">{event.title}</h2>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 mb-4 text-gray-700">
                <div>
                  <p className="text-sm text-gray-500 uppercase font-bold mb-1">Date & Time</p>
                  <p className="font-semibold text-sm sm:text-base">{event.date}</p>
                  <p className="text-xs sm:text-sm">{event.time}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 uppercase font-bold mb-1">Location</p>
                  <p className="font-semibold text-sm sm:text-base">{event.location}</p>
                </div>
              </div>

              <div className="bg-gray-50 rounded-lg p-4 mb-4 border-l-4 border-mcgillRed">
                <p className="text-sm text-gray-500 uppercase font-bold mb-1">Speaker</p>
                <p className="font-semibold text-gray-900 text-sm sm:text-base">{event.speaker}</p>
              </div>

              <p className="text-gray-600 mb-4 leading-relaxed text-sm sm:text-base">{event.description}</p>
              <button className="btn-primary text-sm">Register</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
