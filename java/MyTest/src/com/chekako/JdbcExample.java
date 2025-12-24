package com.chekako;

import java.sql.*;

public class JdbcExample
{
	public static void main2( String[] argv )
	{
		System.out.println( "-------- PostgreSQL " + "JDBC Connection Testing ------------" );

		try
		{
			Class.forName( "org.postgresql.Driver" );
		}
		catch ( ClassNotFoundException e )
		{
			System.out.println( "Where is your PostgreSQL JDBC Driver? " + "Include in your library path!" );
			e.printStackTrace();
			return;
		}

		System.out.println( "PostgreSQL JDBC Driver Registered!" );

		Connection connection = null;

		try
		{
			connection = DriverManager.getConnection( "jdbc:postgresql://127.0.0.1:5432/MyTest", "postgres", "`" );
		}
		catch ( SQLException e )
		{
			System.out.println( "Connection Failed! Check output console" );
			e.printStackTrace();
			return;
		}

		if ( connection == null )
		{
			System.out.println( "Failed to make connection!" );
			return;
		}

		try
		{
			System.out.println( "You made it, take control your database now!" );
			Statement stmt = connection.createStatement();
			String sql = "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) "
					+ "VALUES (1, 'Paul', 32, 'California', 20000.00 );";
			stmt.executeUpdate( sql );

			connection.commit();

			stmt = connection.createStatement();
			ResultSet rs = stmt.executeQuery( "SELECT * FROM COMPANY;" );
			while ( rs.next() )
			{
				int id = rs.getInt( "id" );
				String name = rs.getString( "name" );
				int age = rs.getInt( "age" );
				String address = rs.getString( "address" );
				float salary = rs.getFloat( "salary" );
				System.out.println( "ID = " + id );
				System.out.println( "NAME = " + name );
				System.out.println( "AGE = " + age );
				System.out.println( "ADDRESS = " + address );
				System.out.println( "SALARY = " + salary );
				System.out.println();
			}
			rs.close();
			stmt.close();
			connection.close();
		}
		catch ( SQLException e )
		{
			System.out.println( "Connection Failed! Check output console" );
			e.printStackTrace();
			return;
		}
	}
}
