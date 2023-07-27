channels

pkg load signal
figure(1)
plot(ch1,'r')
hold on
plot(ch2,'b')
disp("filter")

%signal = ((ch1-ch2)-mean(ch1-ch2))(1:20000)

% reverted probe on setup 01 requires inverting
%signal = ch1(1:20000)
signal = -ch1(1:20000)

figure(2)
plot(signal)

fs=200000000
fc_low=20000000

[b_low,a_low] = butter(20,fc_low/(fs/2), "low");
signal_low=filter(b_low,a_low,signal)
figure(3)
plot(signal_low)

fc_high=100000

[b_high, a_high] = butter(6, fc_high/(fs/2), "high")
signal_low_high=filter(b_high,a_high,signal_low)
figure(4)
plot(signal_low_high)

%signal_b = signal;
%signal_b(signal_b > 0.4) = 1;
%signal_b(signal_b <= 0.4) = 0;

for i = 1:length(signal)
    if signal(i) > 0.4
        signal_b(i) = 1;
    elseif signal(i) < 0.4
        signal_b(i)=0;
    else
        if(i==1)
            signal_b(i)=0;
        else
            signal_b(i)=signal_b(i-1);
        end
    end
end

figure(5)
plot(signal_b)

for c = 1:(floor(length(signal_b)+19)/20)
    a(c)=sum(signal_b(20*(c-1)+1:20*c).*2.^[19:-1:0])
end

fileID = fopen('signal.bin','w');
fwrite(fileID,a,'uint32','ieee-le');
fclose(fileID);

%signal_b = signal_low_high;
%signal_b(signal_b > 0.7) = 1;
%signal_b(signal_b <= 0.7) = 0;

for i = 1:length(signal_low_high)
    if signal_low(i) > 0.4
        signal_b(i) = 1;
    elseif signal_low(i) < 0.4
        signal_b(i)=0;
    else
        if(i==1)
            signal_b(i)=0;
        else
            signal_b(i)=signal_b(i-1);
        end
    end
end

figure(6)
plot(signal_b)

for c = 1:(floor(length(signal_b)+19)/20)
    a(c)=sum(signal_b(20*(c-1)+1:20*c).*2.^[19:-1:0])
end

fileID = fopen('signal_f.bin','w');
fwrite(fileID,a,'uint32','ieee-le');
fclose(fileID);
