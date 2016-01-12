package model;

import java.util.ArrayList;
import java.util.List;

public class StoreageMajor {

	public int majorId;
	public String majorName;
	public double salary;
	public int schoolId;
	public List<StoreageComment> comments;
	
	
	
	public double getSalary() {
		return salary;
	}
	public void setSalary(double salary) {
		this.salary = salary;
	}
	public StoreageMajor() {
		super();
		comments = new ArrayList<StoreageComment>();
		// TODO Auto-generated constructor stub
	}
	public int getSchoolId() {
		return schoolId;
	}
	public void setSchoolId(int schoolId) {
		this.schoolId = schoolId;
	}
	public List<StoreageComment> getComments() {
		return comments;
	}
	public void setComments(List<StoreageComment> comments) {
		this.comments = comments;
	}
	public int getMajorId() {
		return majorId;
	}
	public void setMajorId(int majorId) {
		this.majorId = majorId;
	}
	public String getMajorName() {
		return majorName;
	}
	public void setMajorName(String majorName) {
		this.majorName = majorName;
	}
	
	
}
