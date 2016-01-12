package dao;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

import com.mysql.jdbc.Connection;
import com.mysql.jdbc.Statement;

import model.StoreageComment;
import model.StoreageMajor;
import model.StoreageSchool;
import util.SQLUtil;

public class SchoolDAO {

	public static Connection conn = SQLUtil.getConn();
	public static Statement stmt = null;
	public static ResultSet rs = null;
	
	
	public static boolean exitRank(int schoolId) {

		boolean flag = false;

		
		
		try {
			if(stmt == null)
				stmt = (Statement) conn.createStatement();

			String sql = "select * from Rank where schoolid=" + schoolId;
			rs = stmt.executeQuery(sql);
			while (rs.next()) {
				flag = true;
			}

		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
		return flag;
	}
	
	public static boolean exitSchool(String schoolName) {

		boolean flag = false;

		
		
		try {
			if(stmt == null)
				stmt = (Statement) conn.createStatement();

			String sql = "select * from school where schoolName='" + schoolName+"'";
			rs = stmt.executeQuery(sql);
			while (rs.next()) {
				flag = true;
			}

		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
		return flag;
	}
	
	public static boolean exitMajor(String majorName,int schoolId) {

		boolean flag = false;

		Connection conn = SQLUtil.getConn();
		Statement stmt = null;
		ResultSet rs = null;
		try {
			stmt = (Statement) conn.createStatement();

			String sql = "select * from major where majorName='" + majorName+"' and schoolID=" + schoolId;
			rs = stmt.executeQuery(sql);
			while (rs.next()) {
				flag = true;
			}

		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return flag;
	}
	
	public static boolean exitComment(StoreageComment comment) {

		boolean flag = false;

		
		try {
			if(stmt == null)
				stmt = (Statement) conn.createStatement();

			String sql = "select * from comment where majorId="+comment.getMajorId();
			rs = stmt.executeQuery(sql);
			while (rs.next()) {
				flag = true;
			}

		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
		return flag;
	}
	
	public static boolean exitSalary(int majorID) {

		boolean flag = false;

		
		try {
			if(stmt == null)
				stmt = (Statement) conn.createStatement();

			String sql = "select * from comment where majorId=" + majorID;
			rs = stmt.executeQuery(sql);
			while (rs.next()) {
				flag = true;
			}

		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
		return flag;
	}


	
	
	
	public static void saveSchoolRank(List<StoreageSchool> schoolList) {
		
		// TODO Auto-generated method stub

		try {
			if(stmt == null)
				stmt = (Statement) conn.createStatement();
			for(StoreageSchool school : schoolList){
				
				String sql = "";
				if(!exitSchool(school.getSchoolName())){
					continue;
				}
			
				sql = "select schoolId from school where schoolName='" + school.getSchoolName()+"'";
				rs = stmt.executeQuery(sql);
				while (rs.next()) {
					school.setSchoolId(rs.getInt("schoolId"));
				}
				
				if(!exitRank(school.getSchoolId())){
					sql = "insert into rank(schoolId,score) values(" + school.getSchoolId() + ","+school.getScore()+")";
					stmt.executeUpdate(sql);
				}
				
			}
			

		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
		
		System.out.println("save success");
	}

	
	public static void saveSchool(List<StoreageSchool> schoolList) {
		
		// TODO Auto-generated method stub

		try {
			if(stmt == null)
				stmt = (Statement) conn.createStatement();
			for(StoreageSchool school : schoolList){
				
				String sql = "";
				if(!exitSchool(school.getSchoolName())){
					sql = "insert into school(schoolName) values('" + school.getSchoolName() + "')";
					stmt.executeUpdate(sql);
				}
			
				sql = "select schoolId from school where schoolName='" + school.getSchoolName()+"'";
				rs = stmt.executeQuery(sql);
				while (rs.next()) {
					school.setSchoolId(rs.getInt("schoolId"));
				}
				
				for(StoreageMajor major : school.getMajors()){
					if(!exitMajor(major.getMajorName(),school.getSchoolId())){
						sql = "insert into major(majorName,schoolId) values('" + major.getMajorName() + "'," + school.getSchoolId() + ")";
						stmt.executeUpdate(sql);
					}
					
					sql = "select majorId from major where majorName='" +  major.getMajorName()+"' and schoolID="+school.schoolId;
					rs = stmt.executeQuery(sql);
					while (rs.next()) {
						major.setMajorId(rs.getInt("majorId"));
					}
					
				}
			}
			

		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
		
		System.out.println("save success");
	}
	

	public static void saveSalary(List<StoreageSchool> schoolList) {
		
		// TODO Auto-generated method stub

		try {
			if(stmt == null)
				stmt = (Statement) conn.createStatement();
			for(StoreageSchool school : schoolList){
				
				String sql = "";
				if(exitSchool(school.getSchoolName())){
					
					sql = "select schoolId from school where schoolName='" + school.getSchoolName()+"'";
					rs = stmt.executeQuery(sql);
					while (rs.next()) {
						school.setSchoolId(rs.getInt("schoolId"));
					}
					
					for(StoreageMajor major : school.getMajors()){
						if(exitMajor(major.getMajorName(),school.getSchoolId())){

							sql = "select majorId from major where majorName='" +  major.getMajorName()+"' and schoolID="+school.schoolId;
							rs = stmt.executeQuery(sql);
							while (rs.next()) {
								major.setMajorId(rs.getInt("majorId"));
							}
							
							double salary = major.getSalary();
							if(!exitSalary(major.majorId)){
								sql = "insert into salary(majorId,money) values(" +
										major.getMajorId() + "," + salary + ")";
								stmt.executeUpdate(sql);
							}
						}
						
						
					}
				}
			
				
			}
			

		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
		
		System.out.println("save success");
	}
	
	public static void saveComment(List<StoreageSchool> schoolList) {
		
		// TODO Auto-generated method stub

		try {
			if(stmt == null)
				stmt = (Statement) conn.createStatement();
			for(StoreageSchool school : schoolList){
				
				String sql = "";
				if(!exitSchool(school.getSchoolName())){
					sql = "insert into school(schoolName) values('" + school.getSchoolName() + "')";
					stmt.executeUpdate(sql);
				}
			
				sql = "select schoolId from school where schoolName='" + school.getSchoolName()+"'";
				rs = stmt.executeQuery(sql);
				while (rs.next()) {
					school.setSchoolId(rs.getInt("schoolId"));
				}
				
				for(StoreageMajor major : school.getMajors()){
					if(!exitMajor(major.getMajorName(),school.getSchoolId())){
						sql = "insert into major(majorName,schoolId) values('" + major.getMajorName() + "'," + school.getSchoolId() + ")";
						stmt.executeUpdate(sql);
					}
					
					sql = "select majorId from major where majorName='" +  major.getMajorName()+"' and schoolID="+school.schoolId;
					rs = stmt.executeQuery(sql);
					while (rs.next()) {
						major.setMajorId(rs.getInt("majorId"));
					}
					
					StoreageComment comment = major.getComments().get(0);
					if(!exitComment(comment)){
						sql = "insert into comment(majorId,comprehensiveScore,teachingScore,dealScore,workScore) values(" +
								major.getMajorId() + "," + comment.getComprehensiveScore()+ "," + comment.getTeachingScore() +","+
								comment.getDealScore()+","+ comment.getWorkScore() +")";
						stmt.executeUpdate(sql);
					}
					
					
					
				}
			}
			

		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
		
		System.out.println("save success");
	}
	
	public static void close(){

		try {
			if (rs != null) {
				rs.close();
				rs = null;
			}
			if (stmt != null) {
				stmt.close();
				stmt = null;
			}
			if (conn != null) {
				conn.close();
				conn = null;
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
	
}
