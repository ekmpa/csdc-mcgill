export default function LabMeetingsPage() {
  const mockMeetings = [
    {
      id: "1",
      title: "Lab Kickoff: Trust and Democratic Citizenship",
      date: "April 8, 2026 at 12:30 PM",
      speaker: "CSDC Research Team",
      affiliation: "McGill Department of Political Science",
      location: "Leacock Building, Room 232"
    },
    {
      id: "2",
      title: "Survey Design Clinic for Comparative Opinion Research",
      date: "April 15, 2026 at 12:30 PM",
      speaker: "Dr. Samuel Berger",
      affiliation: "McGill CSDC",
      location: "Leacock Building, Room 232"
    },
    {
      id: "3",
      title: "Belonging, Cities, and Political Participation",
      date: "April 22, 2026 at 12:30 PM",
      speaker: "Dr. Nadia Rahman",
      affiliation: "McGill CSDC",
      location: "Leacock Building, Room 232"
    }
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 py-16">
      <h1 className="text-4xl font-bold text-mcgillRed mb-4">Lab Meetings & Seminars</h1>
      <p className="text-lg text-gray-600 mb-12">
        Weekly research meetings featuring works-in-progress, methods clinics, and invited discussants.
      </p>
      
      <div className="space-y-6">
        {mockMeetings.map((meeting) => (
          <div key={meeting.id} className="card border-t-4 border-mcgillRed">
            <h2 className="text-2xl font-bold text-mcgillRed mb-2">{meeting.title}</h2>
            <p className="text-sm text-gray-500 mb-4">📅 {meeting.date}</p>
            
            <div className="bg-gray-50 rounded-lg p-4 mb-4">
              <p className="font-semibold text-gray-900">{meeting.speaker}</p>
              <p className="text-sm text-gray-600">{meeting.affiliation}</p>
            </div>
            
            <p className="text-gray-600 mb-4">📍 {meeting.location}</p>
            <button className="btn-primary">RSVP</button>
          </div>
        ))}
      </div>
    </div>
  );
}
