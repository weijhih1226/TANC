program read_polar_data

implicit none

integer   :: ii
character :: infile*256
character :: head16(16),radarname*4
logical   :: tf
integer   :: header(40),header_int(40)
real      :: header_flt(40)
!!! variables for header !!!
real      :: radar_elev,rlat,rlon,theta,nyquist,azm_sp,gate_sp
integer   :: h_scale,yyyy,mm,dd,hh,mn,ss,nivcp
integer   :: itit,nray,ngate,azm_start,gate_start,var_scale,var_miss,rf_miss
!!! variables for header !!!
integer,allocatable :: ppi2d(:,:)

call getarg(1,infile)
! =================================================================
! === read all ppi data into a 3d array ppi3d(ngate,nray,nelev) ===
! =================================================================
  ! === only read first 160 byte for header information ===
  write(*,*) 'Reading : ',trim(infile)
  open(11,file=trim(infile),form='unformatted',&
          status='old',access='stream')
  !open(11,file=trim(infile),form='binary',status='old')
  read(11) head16
  read(11) header(5:40)
  if ( count(ichar(head16).eq.0).eq.12 ) then
    write(*,*) "reading q2 data"
    radarname = head16(1)//head16(5)//head16(9)//head16(13)
  else
    write(*,*) "reading q3 data"
    radarname = head16(1)//head16(2)//head16(3)//head16(4)
  end if

  ! === print header ===
  !do ii = 1,26
  !  write(*,*) ii,header(ii)
  !enddo
  !stop

  ! === header information ===
  h_scale = header(5)
  header_int = header/h_scale
  header_flt = real(header)/real(h_scale)
  radar_elev = header_flt(6)
  rlat = header_flt(7)
  rlon = header_flt(8)
  yyyy = header_int(9)
  mm = header_int(10)
  dd = header_int(11)
  hh = header_int(12)
  mn = header_int(13)
  ss = header_int(14)
  nyquist = header_flt(15)
  nivcp = header_int(16)
  itit = header(17)      ! for RCWF,RCCG,RCKT,RCHL
  !itit = header_int(17) ! for others
  theta = header_flt(18)
  nray = header_int(19)
  ngate = header_int(20)
  azm_start = header_int(21)
  azm_sp = header_flt(22)
  gate_start = header_int(23)/1000. !!! m to km
  gate_sp = header_flt(24)/1000. !!! m to km
  var_scale = header_int(25)
  var_miss = header_int(26)*var_scale  !!! var_miss = -99900
  rf_miss = -44400                   !!! range folding value (-444)

  !radarname = char(header(1))//char(header(2))//&
  !            char(header(3))//char(header(4))
  allocate(ppi2d(ngate,nray))
  read(11) ppi2d
  close(11)

  write(*,*) '   radarname  = ',radarname
  write(*,*) '05 h_scale    = ',header(5)
  write(*,*) '06 radar_elev = ',header_flt(6)
  write(*,*) '07 rlat       = ',header_flt(7)
  write(*,*) '08 rlon       = ',header_flt(8)
  write(*,*) '09 yyyy       = ',header_int(9)
  write(*,*) '10 mm         = ',header_int(10)
  write(*,*) '11 dd         = ',header_int(11)
  write(*,*) '12 hh         = ',header_int(12)
  write(*,*) '13 mn         = ',header_int(13)
  write(*,*) '14 ss         = ',header_int(14)
  write(*,*) '15 nyquist    = ',header_flt(15)
  write(*,*) '16 nivcp      = ',header_int(16)
  write(*,*) '17 itit       = ',header_int(17)
  write(*,*) '18 theta      = ',header_flt(18)
  write(*,*) '19 nray       = ',header_int(19)
  write(*,*) '20 ngate      = ',header_int(20)
  write(*,*) '21 azm_start  = ',header_flt(21)
  write(*,*) '22 azm_sp     = ',header_flt(22)
  write(*,*) '23 gate_start = ',header_flt(23)
  write(*,*) '24 gate_sp    = ',header_flt(24)
  write(*,*) '25 var_scale  = ',header_int(25)
  write(*,*) '26 var_miss   = ',header_int(26)

  write(*,*) minval(ppi2d),maxval(ppi2d)
  write(*,*) minval(ppi2d,ppi2d.ne.-999*var_scale),maxval(ppi2d)
  write(*,*) minval(ppi2d,ppi2d.ne.-999*var_scale .and. ppi2d.ne.-99*var_scale),maxval(ppi2d)
  !write(*,*) ppi2d

  deallocate(ppi2d)
end
