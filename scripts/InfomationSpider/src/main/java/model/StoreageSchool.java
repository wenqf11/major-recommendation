package model;

import java.util.ArrayList;
import java.util.List;

public class StoreageSchool {

	public int schoolId;
	public String schoolName;
	public double score;
	public List<StoreageMajor> majors;
	
	
	
	public double getScore() {
		return score;
	}
	public void setScore(double score) {
		this.score = score;
	}
	public StoreageSchool() {
		super();
		majors = new ArrayList<StoreageMajor>();
		// TODO Auto-generated constructor stub
	}
	public List<StoreageMajor> getMajors() {
		return majors;
	}
	public void setMajors(List<StoreageMajor> majors) {
		this.majors = majors;
	}
	public int getSchoolId() {
		return schoolId;
	}
	public void setSchoolId(int schoolId) {
		this.schoolId = schoolId;
	}
	public String getSchoolName() {
		return schoolName;
	}
	public void setSchoolName(String schoolName) {
		this.schoolName = schoolName;
	}
	
	
}
