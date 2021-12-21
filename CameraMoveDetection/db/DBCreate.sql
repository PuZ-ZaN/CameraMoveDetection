USE [CameraMoveDetection]
GO

/****** Object:  Table [dbo].[Camera]    Script Date: 20.12.2021 20:33:49 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/*Drop table Camera;*/
CREATE TABLE Camera(
	CameraId [int] primary key identity(1,1) NOT NULL,
	Name [varchar](50) unique NOT NULL,
	Url [varchar](200) unique NOT NULL,
	isMovingBorder [int] NOT NULL,
	isMovedBorder [int] NOT NULL,
)
GO

create table Signal(
	SignalID int primary key not null,
	[CameraId] [int] foreign key references dbo.Camera NOT NULL,
	[Image] text not null,
	[TimeStamp] datetime not null,
	[isMoved] bit Default "false" not null,
	[isMoving] bit Default "false" not null
)
go


