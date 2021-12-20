USE [CameraMoveDetection]
GO

/****** Object:  Table [dbo].[Camera]    Script Date: 20.12.2021 20:33:49 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Camera](
	[CameraId] [int] NOT NULL,
	[Name] [varchar](50) NOT NULL,
	[Url] [varchar](200) NOT NULL,
	isMovingBorder [int] NOT NULL,
	isMovedBorder [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[CameraId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


