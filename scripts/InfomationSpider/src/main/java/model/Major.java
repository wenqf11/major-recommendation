package model;

import java.util.HashMap;
import java.util.Map;

public class Major {

	private String specialtyname;
	
	private String localProvince;
	private String studentType;
	private String year;
	private String batch;
	private String var;
	private String var_score;
	private String max;
	private String min;
	private String zyid;
	private String url;
	private String seesigh;
	private Map<String,Double> scoreLine = new HashMap<String,Double>();
	
	
	
	
	public Major() {
		
		this.specialtyname = "";
		// TODO Auto-generated constructor stub
	}
	public Map<String, Double> getScoreLine() {
		return scoreLine;
	}
	public void setScoreLine(Map<String, Double> scoreLine) {
		this.scoreLine = scoreLine;
	}
	public String getLocalProvince() {
		return localProvince;
	}
	public void setLocalProvince(String localProvince) {
		this.localProvince = localProvince;
	}
	public String getStudentType() {
		return studentType;
	}
	public void setStudentType(String studentType) {
		this.studentType = studentType;
	}
	public String getYear() {
		return year;
	}
	public void setYear(String year) {
		this.year = year;
	}
	public String getBatch() {
		return batch;
	}
	public void setBatch(String batch) {
		this.batch = batch;
	}
	public String getVar() {
		return var;
	}
	public void setVar(String var) {
		this.var = var;
	}
	public String getVar_score() {
		return var_score;
	}
	public void setVar_score(String var_score) {
		this.var_score = var_score;
	}
	public String getMax() {
		return max;
	}
	public void setMax(String max) {
		this.max = max;
	}
	public String getMin() {
		return min;
	}
	public void setMin(String min) {
		this.min = min;
	}
	
	public String getUrl() {
		return url;
	}
	public void setUrl(String url) {
		this.url = url;
	}
	public String getSpecialtyname() {
		return specialtyname;
	}
	public void setSpecialtyname(String specialtyname) {
		this.specialtyname = specialtyname;
	}
	@Override
	public boolean equals(Object obj) {
		// TODO Auto-generated method stub
		boolean flag = true;
		if (obj instanceof Major) {
			
			Major compareMajor = (Major) obj;
			
			
			flag = compareMajor.getStudentType().equals(this.studentType)&&compareMajor.getSpecialtyname().equals(this.specialtyname) && compareMajor.getLocalProvince().equals(this.localProvince) && compareMajor.getYear().equals(this.year);
			
		}else
			flag = false;
		
		return flag;
	}
	public String getZyid() {
		return zyid;
	}
	public void setZyid(String zyid) {
		this.zyid = zyid;
	}
	public String getSeesigh() {
		return seesigh;
	}
	public void setSeesigh(String seesigh) {
		this.seesigh = seesigh;
	}
	
	
}
