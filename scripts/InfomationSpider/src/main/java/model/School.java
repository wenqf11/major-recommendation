package model;

import java.util.ArrayList;
import java.util.List;

public class School {



	private String schooleID;
	private String schoolName;
	
	private List<Major>majorList = new ArrayList<Major>();
	public List<Major>majorList2 = new ArrayList<Major>();

	public String getSchooleID() {
		return schooleID;
	}

	public void setSchooleID(String schooleID) {
		this.schooleID = schooleID;
	}

	public String getSchoolName() {
		return schoolName;
	}

	public void setSchoolName(String schoolName) {
		this.schoolName = schoolName;
	}

	public List<Major> getMajorList() {
		return majorList;
	}

	public void setMajorList(List<Major> majorList) {
		this.majorList = majorList;
	}
	@Override
	public boolean equals(Object obj) {
		// TODO Auto-generated method stub
		boolean flag = false;
		if (obj instanceof School) {
			School school = (School) obj;
			
			flag = school.getSchoolName().equals(this.getSchoolName());
		}
		return flag;
	}
	
	
}
