USE [CameraMoveDetection]
GO

/****** Object:  Table [dbo].[Camera]    Script Date: 20.12.2021 20:33:49 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/*Drop table Camera;*/
CREATE TABLE Camera(
	[CameraId] int primary key identity(1,1) NOT NULL,
	[Name] varchar(50) unique NOT NULL,
	[Url] text NOT NULL,
	[IsMovingBorder] int NOT NULL,
	[IsMovedBorder] int NOT NULL
)
GO

create table Signal(
	[CameraId] [int] foreign key references dbo.Camera NOT NULL,
	[SmallTimeStamp] datetime not null,
	[isMoved] bit Default 0 not null,
	[isMoving] bit Default 0 not null,
	[Image] text not null,
	Constraint PK_Clustered_CameraId_TimeStamp primary key clustered (CameraId,TimeStamp)
)
go


