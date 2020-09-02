using Microsoft.WindowsAPICodePack.Dialogs;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Windows;

namespace WpfApp2
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }        
        internal static Dictionary<string, string> prodDetails = new Dictionary<string, string>();
        public static void ExecuteCommand(string command,ref string stdoutputres)
        {
            var processInfo = new ProcessStartInfo("cmd.exe", "/c " + command);
            processInfo.CreateNoWindow = true;
            processInfo.UseShellExecute = false;
            processInfo.RedirectStandardError = true;
            processInfo.RedirectStandardOutput = true;

            var process = Process.Start(processInfo);
            process.OutputDataReceived += (object sender, DataReceivedEventArgs e) =>
            process.BeginOutputReadLine();
            stdoutputres = process.StandardOutput.ReadToEnd();
            process.ErrorDataReceived += (object sender, DataReceivedEventArgs e) =>
            process.BeginErrorReadLine();

            process.WaitForExit();

            Console.WriteLine("ExitCode: {0}", process.ExitCode);
            process.Close();
        }
        private void SaadChecinkButtonClick(object sender, RoutedEventArgs e)
        {
            //ExecuteCommand("python checkin_saaad.bat " + prodDetails["productName"] +" "+ prodDetails["oem"]);
        }

        private void BrwoseButtonClick(object sender, RoutedEventArgs e)
        {
            CommonOpenFileDialog dialog = new CommonOpenFileDialog();
            dialog.InitialDirectory = Directory.GetCurrentDirectory();
            dialog.IsFolderPicker = true;
            if (dialog.ShowDialog() == CommonFileDialogResult.Ok)
            {
                txtREleaseNotesLoc.Text = Path.GetFileName(dialog.FileName);
            }
        }
        private void PcikConfigspec(object sender, RoutedEventArgs e)
        {
            txtconfigspec.Text = "";
            string prodDetaislstout = "";                        
            ExecuteCommand("python FetchDetailsWithFITID.py " + txtFITID.Text, ref prodDetaislstout);
            JObject prodDetaislJson = JObject.Parse(prodDetaislstout);
            foreach (var prop in prodDetaislJson.Properties())
            {
                prodDetails.Add(prop.Name, prop.Value.ToString());
            }
            txtconfigspec.Text = prodDetails["configspec"];
        }
        
    }
}
