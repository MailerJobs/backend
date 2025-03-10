// @ts-nocheck
import React, { useEffect, useState, useContext } from "react";
import { toast } from "react-toastify";
import { JobIndex } from "../components/context/job_list_context";
import { format } from "date-fns";

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

const JobFairDataByCollegeName = () => {
  const [selectedCollege, setSelectedCollege] = useState("");
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(false);
  const { clientLogin } = useContext(JobIndex);

  useEffect(() => {
    if (selectedCollege) {
      fetchStudentData();
    }
  }, [selectedCollege]);

  // Fetching student data based on college name
  const fetchStudentData = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${BASE_URL}jobfair/${selectedCollege}`);
      if (!response.ok) throw new Error("Failed to fetch student data");

      const result = await response.json();
      console.log("API Response:", result); // Debugging

      if (!result.students || !Array.isArray(result.students)) {
        throw new Error("Unexpected API response format");
      }

      const formattedData = result.students.map((student, index) => ({
        id: student.id || index + 1, // Ensure unique IDs
        full_name: student.name || "N/A", // Display full name
        dob: student.dob ? format(new Date(student.dob), "dd/MM/yyyy") : "N/A", // Format DOB
        gender: student.gender || "N/A",
        phone: student.phone || "N/A",
        email: student.email || "N/A",
        institution: student.institution || "N/A",
        degree: student.degree || "N/A",
        graduation_year: student.graduation_year || "N/A",
        reg_no: student.reg_no || "N/A",
        resume_url: student.resume_name || "N/A", // Display resume URL
        english_proficiency: student.english_proficiency || "N/A", // Add English proficiency
        hindi_proficiency: student.hindi_proficiency || "N/A", // Add Hindi proficiency
        backlog_status: student.backlog_status || "N/A", // Add backlog status
      }));

      setStudents(formattedData);
    } catch (error) {
      toast.error("Error fetching student data", { position: "top-center" });
      console.error("Student Fetch Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleCollegeChange = (e) => setSelectedCollege(e.target.value);

  const handleSubmit = () => {
    if (selectedCollege.trim() === "") {
      toast.error("Please enter a college name", { position: "top-center" });
    } else {
      fetchStudentData();
    }
  };

  return (
    <div className="w-full max-w-7xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-3xl font-bold mb-6 text-center text-black">
        Student Details by College Name
      </h2>

      {/* College input */}
      <div className="mb-4 flex justify-center">
        <input
          type="text"
          className="p-3 border border-gray-300 rounded-lg w-1/2"
          placeholder="Enter College Name"
          value={selectedCollege}
          onChange={handleCollegeChange}
        />
      </div>

      {/* Submit Button */}
      <div className="mb-6 flex justify-center">
        <button
          onClick={handleSubmit}
          className="p-3 bg-blue-500 text-white rounded-lg"
        >
          Submit
        </button>
      </div>

      {/* Data display */}
      {clientLogin ? (
        loading ? (
          <div className="flex justify-center items-center h-32">
            <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-gray-900"></div>
          </div>
        ) : (
          <table className="w-full border-collapse border border-gray-300">
            <thead>
              <tr className="bg-gray-200 text-left">
                <th className="border p-3 text-center">ID</th>
                <th className="border p-3">Full Name</th>
                <th className="border p-3">Date of Birth</th>
                <th className="border p-3">Gender</th>
                <th className="border p-3">Phone</th>
                <th className="border p-3">Email</th>
                <th className="border p-3">Institution</th>
                <th className="border p-3">Degree</th>
                <th className="border p-3">Graduation Year</th>
                <th className="border p-3">Register Number</th>
                <th className="border p-3">Resume</th>
                <th className="border p-3">English Proficiency</th>
                <th className="border p-3">Hindi Proficiency</th>
                <th className="border p-3">Backlog Status</th>
              </tr>
            </thead>
            <tbody>
              {students.length > 0 ? (
                students.map((student, index) => (
                  <tr key={index} className="text-center">
                    <td className="border p-3">{student.id}</td>
                    <td className="border p-3">{student.full_name}</td>
                    <td className="border p-3">{student.dob}</td>
                    <td className="border p-3">{student.gender}</td>
                    <td className="border p-3">{student.phone}</td>
                    <td className="border p-3">{student.email}</td>
                    <td className="border p-3">{student.institution}</td>
                    <td className="border p-3">{student.degree}</td>
                    <td className="border p-3">{student.graduation_year}</td>
                    <td className="border p-3">{student.reg_no}</td>
                    <td className="border p-3">
                      <a href={student.resume_url} target="_blank" rel="noopener noreferrer">
                        Resume
                      </a>
                    </td>
                    <td className="border p-3">{student.english_proficiency}</td>
                    <td className="border p-3">{student.hindi_proficiency}</td>
                    <td className="border p-3">{student.backlog_status}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="14" className="border p-4 text-center text-gray-500">
                    No student data found
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        )
      ) : (
        <div className="text-center py-10">
          <h1 className="text-2xl font-bold text-red-500">
            Please log in to view student details
          </h1>
        </div>
      )}
    </div>
  );
};

export default JobFairDataByCollegeName;
