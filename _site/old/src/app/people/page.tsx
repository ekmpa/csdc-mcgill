export default function PeoplePage() {
  const placeholderBio =
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.";

  const mockProfiles = [
    {
      id: "1",
      name: "Elissa Berwick",
      title: "Faculty Member",
      affiliation: "Department of Political Science",
      bio: placeholderBio,
      photo: "https://via.placeholder.com/200",
      expertise: ["Political Science", "Democratic Citizenship", "Civic Life"]
    },
    {
      id: "2",
      name: "Aaron Erlich",
      title: "Faculty Member",
      affiliation: "Department of Political Science",
      bio: placeholderBio,
      photo: "https://via.placeholder.com/200",
      expertise: ["Political Institutions", "Citizenship", "Comparative Politics"]
    },
    {
      id: "3",
      name: "Benjamin Forest",
      title: "Faculty Member",
      affiliation: "Department of Geography",
      bio: placeholderBio,
      photo: "https://via.placeholder.com/200",
      expertise: ["Human Geography", "Urban Studies", "Inclusion"]
    },
    {
      id: "4",
      name: "Eric Hehman",
      title: "Faculty Member",
      affiliation: "Department of Psychology",
      bio: placeholderBio,
      photo: "https://via.placeholder.com/200",
      expertise: ["Psychology", "Social Attitudes", "Behavior"]
    },
    {
      id: "5",
      name: "Juan Pablo Luna",
      title: "Faculty Member",
      affiliation: "Department of Political Science",
      bio: placeholderBio,
      photo: "https://via.placeholder.com/200",
      expertise: ["Representation", "Parties", "Democratic Governance"]
    },
    {
      id: "6",
      name: "Reihaneh Rabbany",
      title: "Faculty Member",
      affiliation: "Department of Computer Science",
      bio: placeholderBio,
      photo: "https://via.placeholder.com/200",
      expertise: ["Computational Social Science", "Networks", "Data Science"]
    },
    {
      id: "7",
      name: "Eran Shor",
      title: "Faculty Member",
      affiliation: "Department of Sociology",
      bio: placeholderBio,
      photo: "https://via.placeholder.com/200",
      expertise: ["Sociology", "Inequality", "Media and Society"]
    },
    {
      id: "8",
      name: "Thomas Soehl",
      title: "Faculty Member",
      affiliation: "Department of Sociology",
      bio: placeholderBio,
      photo: "https://via.placeholder.com/200",
      expertise: ["Migration", "Identity", "Social Integration"]
    },
    {
      id: "9",
      name: "Prof. Dietlind Stolle",
      title: "Director, McGill CSDC",
      affiliation: "Department of Political Science",
      bio: placeholderBio,
      photo: "https://via.placeholder.com/200",
      expertise: ["Social Trust", "Political Behavior", "Democratic Participation"]
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-white">
      <div className="max-w-6xl mx-auto px-4 py-16">
      <h1 className="text-4xl font-bold text-mcgillRed mb-2">Our Research Team</h1>
      <p className="text-lg text-gray-600 mb-12">
        Meet the researchers, postdoctoral fellows, and graduate trainees advancing democratic citizenship research at McGill.
      </p>
      
      <div className="grid grid-cols-1 gap-6">
        {mockProfiles.map((profile) => (
          <div
            key={profile.id}
            className="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition p-6"
          >
            <div className="flex gap-6">
              <div className="flex-shrink-0">
                <div className="w-32 h-32 bg-gray-200 rounded-lg flex items-center justify-center overflow-hidden">
                  <img
                    src={profile.photo}
                    alt={profile.name}
                    className="w-full h-full object-cover"
                  />
                </div>
              </div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-gray-900 mb-1">{profile.name}</h2>
                <p className="text-mcgillRed font-semibold mb-1">{profile.title}</p>
                <p className="text-sm text-gray-500 mb-3">{profile.affiliation}</p>
                <p className="text-gray-700 leading-relaxed mb-4">{profile.bio}</p>
                <div>
                  <p className="text-xs font-bold text-gray-600 uppercase mb-2">Research Areas</p>
                  <div className="flex flex-wrap gap-2">
                    {profile.expertise.map((area, idx) => (
                      <span key={idx} className="bg-mcgillRed text-white text-xs px-3 py-1 rounded-full">
                        {area}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
    </div>
  );
}
